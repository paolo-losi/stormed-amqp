import struct

from stormed.serialization import parse_method, dump_method

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
        else:
            self.payload = payload
            self.frame_type = frame_type

    def __repr__(self):
        return '<Frame(type=%r, channel=%d, size=%d)>' % (self.frame_type,
                                                          self.channel,
                                                          self.size)        

def from_method(method, channel=0):
    payload = dump_method(method)
    header = frame_header.pack('\x01', channel, len(payload))
    return '%s%s%s' % (header, payload, '\xCE')
