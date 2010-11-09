import socket
from tornado.iostream import IOStream
from tornado.ioloop import IOLoop
from tornado import stack_context

from stormed.util import Enum
from stormed.frame import FrameReader
from stormed.serialization import parse_method

status = Enum('HANDSHAKE', 'CONNECTED', 'CLOSED')

class Connection(object):

    def __init__(self, host, port=5672, io_loop=None):
        self.host = host
        self.port = port
        self.io_loop = io_loop or IOLoop.instance()
        self.stream = None
        self.on_connect_callback = None
        self.status = status.CLOSED

    def connect(self, callback):
        if self.status is not status.CLOSED:
            raise Exception('Connection status is %s' % self.status)
        self.status = status.HANDSHAKE
        self.on_connect_callback = stack_context.wrap(callback)
        self.stream = IOStream(socket.socket(), io_loop=self.io_loop)
        self.stream.connect((self.host, self.port), self._handshake)

    def _handshake(self):
        self.stream.write('AMQP\x00\x00\x09\x01')
        FrameReader(self.stream, self._frame_loop)

    def _frame_loop(self, frame):
        print frame
        if frame.frame_type == '\x01':
            parse_method(frame.payload)
            self.on_connect_callback()
        FrameReader(self.stream, self._frame_loop)

    def close(self):
        self.stream.close()
        self.stream = None
        self.status = status.CLOSED
