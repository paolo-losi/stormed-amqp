import struct

from stormed.message import MessageBuilder
from stormed.serialization import parse_method, dump_method, \
                                  parse_content_header, dump_content_header

frame_header = struct.Struct('!cHL')

class FramingError(Exception): pass

class FrameReader(object):

    def __init__(self, stream, callback):
        self.stream = stream
        self.callback = callback
        self.frame = None
        self._read_header()

    def _read_header(self):
        self.stream.read_bytes(7, self._with_header)

    def _with_header(self, header):
        frame_type, channel, size = frame_header.unpack(header)
        #TODO assert frame_type
        self.frame = Frame(frame_type, channel, size)
        self.stream.read_bytes(size+1, self._with_payload)

    def _with_payload(self, payload_with_end):
        payload = payload_with_end[:-1]
        frame_end = payload_with_end[-1]
        if frame_end != '\xCE': #TODO use AMQP constants
            raise FramingError('unexpected frame end')
        self.frame.set_payload(payload)
        self.callback(self.frame)

class Frame(object):

    def __init__(self, frame_type, channel, size):
        self.channel = channel
        self.size = size
        self.payload = None
        self.frame_type = frame_type

    def set_payload(self, payload):
        if self.frame_type == '\x01':
            self.payload = parse_method(payload)
            self.frame_type = 'method'
        elif self.frame_type == '\x02':
            self.payload = parse_content_header(payload)
            self.frame_type = 'content_header'
        elif self.frame_type == '\x03':
            self.payload = payload
            self.frame_type = 'content_body'
        else:
            #FIXME logging instead of exception
            raise ValueError('unsupported frame type')

    def __repr__(self):
        return '<Frame(type=%r, channel=%d, size=%d)>' % (self.frame_type,
                                                          self.channel,
                                                          self.size)        

def from_method(method, channel=0):
    payload = dump_method(method)
    header = frame_header.pack('\x01', channel, len(payload))
    return '%s%s%s' % (header, payload, '\xCE')

def content_header_from_msg(msg, channel):
    payload = dump_content_header(msg)
    header = frame_header.pack('\x02', channel, len(payload))
    return '%s%s%s' % (header, payload, '\xCE')

def body_frames_from_msg(msg, channel):
    max_size = 2**16 #FIXME should be set by connection negotiation
    frames = []
    for offset in range(0, len(msg.encoded_body), max_size):
        payload = msg.encoded_body[offset:offset + max_size]
        header = frame_header.pack('\x03', channel, len(payload))
        frames.append('%s%s%s' % (header, payload, '\xCE'))
    return frames

class FrameHandler(object):

    def __init__(self, connection):
        self.conn = connection
        self._method_queue = []
        self._pending_meth = None
        self._pending_cb = None
        self._msg_builder = None

    def process_frame(self, frame):
        processor = getattr(self, 'process_'+frame.frame_type)
        processor(frame.payload)

    def process_method(self, method):
        self._msg_builder = None
        pending_meth = self._pending_meth
        if pending_meth and method._name.startswith(pending_meth._name):
            if not method._content:
                if hasattr(method, 'handle'):
                    method.handle(self)
                if self._pending_cb:
                    kargs = dict( (f, getattr(method, f))
                                  for f, _ in method._fields )
                    self._pending_cb(**kargs)
                self._flush()
            else:
                self._msg_builder = MessageBuilder(content_method=method)
        else:
            if hasattr(method, 'handle'):
                method.handle(self)
            else:
                pass # FIXME WARNING

    def process_content_header(self, ch):
        self._msg_builder.add_content_header(ch)

    def process_content_body(self, cb):
        # FIXME better error checking
        self._msg_builder.add_content_body(cb)
        if self._msg_builder.msg_complete:
            msg = self._msg_builder.get_msg()
            if self._pending_cb:
                self._pending_cb(msg)
            self._flush()

    def send_method(self, method, callback=None, message=None):
        self._method_queue.append( (method, callback, message) )
        if not self._pending_meth:
            self._flush()

    def _flush(self):
        self._pending_cb = None
        self._pending_meth = None
        while self._pending_meth is None and self._method_queue:
            method, callback, msg = self._method_queue.pop(0)
            self.write_method(method)
            if msg:
                self.write_msg(msg)
            if method._sync:
                self._pending_meth = method
                self._pending_cb = callback
            else:
                if callback is not None:
                    callback()

    def write_method(self, method):
        f = from_method(method, self.channel_id)
        self.conn.stream.write(f)

    def write_msg(self, msg):
        frames = []
        frames.append(content_header_from_msg(msg, self.channel_id))
        frames.extend(body_frames_from_msg(msg, self.channel_id))
        for f in frames:
            self.conn.stream.write(f)
