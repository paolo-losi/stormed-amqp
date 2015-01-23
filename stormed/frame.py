import struct

from stormed.util import Enum, AmqpError, AmqpStatusError, logger
from stormed.message import MessageBuilder
from stormed.serialization import parse_method, dump_method, \
                                  parse_content_header, dump_content_header

status = Enum('OPENING', 'OPENED', 'CLOSED', 'CLOSING')

frame_header = struct.Struct('!cHL')

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
            raise AmqpError('unexpected frame end')
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
        elif self.frame_type == '\x08':
            self.frame_type = 'heartbeat'
        else:
            #FIXME logging instead of exception
            raise ValueError('unsupported frame type')

    def __repr__(self):
        return '<Frame(type=%r, channel=%d, size=%d)>' % (self.frame_type,
                                                          self.channel,
                                                          self.size)

def from_method(method, ch):
    payload = dump_method(method)
    header = frame_header.pack('\x01', ch.channel_id, len(payload))
    return '%s%s%s' % (header, payload, '\xCE')

def content_header_from_msg(msg, ch):
    payload = dump_content_header(msg)
    header = frame_header.pack('\x02', ch.channel_id, len(payload))
    return '%s%s%s' % (header, payload, '\xCE')

def body_frames_from_msg(msg, ch):
    max_size = ch.conn.frame_max - frame_header.size - 1 # 1 -> end marker size
    frames = []
    for offset in range(0, len(msg.body), max_size):
        payload = msg.body[offset:offset + max_size]
        header = frame_header.pack('\x03', ch.channel_id, len(payload))
        frames.append('%s%s%s' % (header, payload, '\xCE'))
    return frames

HEARTBEAT = '\x08\x00\x00\x00\x00\x00\x00\xCE'

class FrameHandler(object):

    def __init__(self, connection):
        self.conn = connection
        self.status = status.CLOSED
        self._method_queue = []
        self._pending_meth = None
        self._pending_cb = None
        self._msg_builder = None

    @property
    def message(self):
        return self._msg_builder.get_msg()

    @property
    def callback(self):
        return self._pending_cb

    def invoke_callback(self, *args, **kargs):
        if self._pending_cb:
            try:
                self._pending_cb(*args, **kargs)
            except Exception:
                logger.error('Error in callback for %s', self._pending_meth,
                                                         exc_info=True)
            self._pending_cb = None

    def process_frame(self, frame):
        processor = getattr(self, 'process_'+frame.frame_type)
        processor(frame.payload)

    def process_method(self, method):
        if method._content:
            self._msg_builder = MessageBuilder(content_method=method)
        else:
            self._msg_builder = None
            self.handle_method(method)

    def process_content_header(self, ch):
        self._msg_builder.add_content_header(ch)

    def process_content_body(self, cb):
        # FIXME better error checking
        self._msg_builder.add_content_body(cb)
        if self._msg_builder.msg_complete:
            self.handle_method(self._msg_builder.content_method)

    def process_heartbeat(self, hb):
        self.conn.stream.write(HEARTBEAT)

    def handle_method(self, method):
        pending_meth = self._pending_meth
        if hasattr(method, 'handle'):
            try:
                method.handle(self)
            except AmqpError:
                logger.error('Error while handling %s', method, exc_info=True)
                self.reset()
                return
        if pending_meth and method._name.startswith(pending_meth._name):
            self.invoke_callback()
            self._flush()

    def send_method(self, method, callback=None, message=None):
        if self.status == status.CLOSED:
            raise AmqpStatusError('cannot send on a closed %s' %
                                  type(self).__name__)
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
        f = from_method(method, self)
        self.conn.stream.write(f)

    def write_msg(self, msg):
        frames = []
        frames.append(content_header_from_msg(msg, self))
        frames.extend(body_frames_from_msg(msg, self))
        self.conn.stream.write(''.join(frames))

    def reset(self):
        self.status = status.CLOSED
        self._method_queue = []
        self._pending_meth = None
        self._pending_cb = None
        self._msg_builder = None
