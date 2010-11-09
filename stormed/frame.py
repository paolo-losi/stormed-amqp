import struct

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
        frame_type, channel, size = struct.unpack('!cHL', header)
        #TODO assert frame_type
        self.frame = Frame(frame_type, channel, size, None)
        self.stream.read_bytes(size+1, self._with_payload)

    def _with_payload(self, payload_with_end):
        payload = payload_with_end[:-1]
        frame_end = payload_with_end[-1]
        if frame_end != '\xCE':
            raise FramingError('unexpected frame end')
        self.frame.payload = payload
        self.callback(self.frame)

class Frame(object):

    def __init__(self, frame_type, channel, size, payload):
        self.frame_type = frame_type
        self.channel = channel
        self.size = size
        self.payload = payload

    def __repr__(self):
        return '<Frame(type=%r, channel=%d, size=%d)>' % (self.frame_type,
                                                          self.channel,
                                                          self.size)        
