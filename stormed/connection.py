import socket
from tornado.iostream import IOStream
from tornado.ioloop import IOLoop
from tornado import stack_context

from stormed.frame import FrameReader, FrameHandler
from stormed import frame
from stormed.serialization import parse_method, table2str
from stormed.channel import Channel
from stormed.method.connection import status, Close


class Connection(FrameHandler):

    def __init__(self, host, username='guest', password='guest', vhost='/',
                       port=5672, io_loop=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost
        self.io_loop = io_loop or IOLoop.instance()
        self.stream = None
        self.status = status.CLOSED
        self.channels = [self]
        self.channel_id = 0
        self.on_connect_callback = None
        super(Connection, self).__init__(connection=self)

    def connect(self, callback):
        if self.status is not status.CLOSED:
            raise Exception('Connection status is %s' % self.status)
        self.status = status.HANDSHAKE
        self.stream = IOStream(socket.socket(), io_loop=self.io_loop)
        self.stream.connect((self.host, self.port), self._handshake)
        self.on_connect_callback = callback

    def close(self, callback=None):
        #FIXME close all channel to flush _sync_method_queue
        _close = Close(reply_code=0, reply_text='', class_id=0, method_id=0)
        self.send_method(_close, callback)
        self.status = status.CLOSING

    def channel(self, callback=None):
        ch = Channel(channel_id=len(self.channels), conn=self)
        self.channels.append(ch)
        ch.open(callback)
        return ch

    def _handshake(self):
        self.stream.write('AMQP\x00\x00\x09\x01')
        FrameReader(self.stream, self._frame_loop)

    def _frame_loop(self, frame):
        self.channels[frame.channel].handle_frame(frame)
        if self.stream:
            FrameReader(self.stream, self._frame_loop)
