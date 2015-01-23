import time
import socket

from tornado.iostream import IOStream
from tornado.ioloop import IOLoop

from stormed.util import logger, AmqpStatusError
from stormed.frame import FrameReader, FrameHandler, status
from stormed.channel import Channel
from stormed.method.connection import Close

TORNADO_1_2 = hasattr(IOStream, 'connect')

class Connection(FrameHandler):
    """A "physical" TCP connection to the AMQP server

    heartbeat: int, optional
               the requested time interval in seconds for heartbeat frames.

    Connection.on_error callback, when set, is called in case of
    "hard" AMQP Error. It receives a ConnectionErrorinstance as argument:

        def handle_error(conn_error):
            print conn_error.method
            print conn_error.reply_code

        conn.on_error = handle_error

    Connection.on_disconnect callback, when set, is called in case of
    heartbeat timeout or TCP low level disconnection. It receives no args.
    """

    def __init__(self, host, username='guest', password='guest', vhost='/',
                       port=5672, heartbeat=0, io_loop=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost
        self.heartbeat = heartbeat
        self.last_received_frame = None
        self.frame_max = 0
        self.io_loop = io_loop or IOLoop.instance()
        self.stream = None
        self.channels = {0: self}
        self.last_channel_id = 0
        self.channel_id = 0
        self.on_connect = None
        self.on_disconnect = None
        self.on_error = None
        self._close_callback = None
        self._frame_count = 0
        super(Connection, self).__init__(connection=self)

    def connect(self, callback):
        """open the connection to the server"""
        if self.status is not status.CLOSED:
            raise AmqpStatusError('Connection status is %s' % self.status)
        self.status = status.OPENING
        sock = socket.socket()
        sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        self.on_connect = callback
        if TORNADO_1_2:
            self.stream = IOStream(sock, io_loop=self.io_loop)
            self.stream.set_close_callback(self.on_closed_stream)
            self.stream.connect((self.host, self.port), self._handshake)
        else:
            sock.connect((self.host, self.port))
            self.stream = IOStream(sock, io_loop=self.io_loop)
            self.stream.set_close_callback(self.on_closed_stream)
            self._handshake()

    def close(self, callback=None):
        """cleanly closes the connection to the server.

        all pending tasks are flushed before connection shutdown"""

        if self.status not in (status.OPENING, status.OPENED):
            raise AmqpStatusError('connection is not open')

        self._close_callback = callback
        self.status = status.CLOSING

        for ch in self.channels.values():
            if ch is not self and ch.status in (status.OPENING, status.OPENED):
                ch.close(self.close)

        m = Close(reply_code=0, reply_text='', class_id=0, method_id=0)
        self.send_method(m, self._close_callback)

    def _get_next_channel_id(self):
        if len(self.channels) == 0x10000:
            raise AmqpError('max channels per connection exceeded')

        next_id = self.last_channel_id
        while True:
            next_id = (next_id + 1) % 0x10000
            if next_id not in self.channels:
                break

        self.last_channel_id = next_id
        return next_id

    def channel(self, callback=None):
        """get a Channel instance"""
        if self.status == status.OPENED:
            ch_id = self._get_next_channel_id()
            ch = Channel(channel_id=ch_id, conn=self)
            self.channels[ch_id] = ch
            ch._open(callback)
            return ch
        else:
            raise AmqpStatusError('connection is not opened')

    def _handshake(self):
        self.stream.write('AMQP\x00\x00\x09\x01')
        FrameReader(self.stream, self._frame_loop)

    def _frame_loop(self, frame):
        if self.heartbeat:
            self.last_received_frame = time.time()
        self.channels[frame.channel].process_frame(frame)
        self._frame_count += 1
        if self.stream:
            # Every 5 frames ioloop gets the control back in order
            # to avoid hitting the recursion limit
            # reading one frame cost 13 levels of stack recursion
            # TODO check if always using _callbacks is faster that frame
            # counting
            if self._frame_count == 5:
                self._frame_count = 0
                cb = lambda: FrameReader(self.stream, self._frame_loop)
                self._add_ioloop_callback(cb)
            else:
                FrameReader(self.stream, self._frame_loop)

    if TORNADO_1_2:
        def _add_ioloop_callback(self, callback):
            self.io_loop._callbacks.append(callback)
    else:
        def _add_ioloop_callback(self, callback):
            self.io_loop._callbacks.add(callback)

    def close_stream(self):
        if self.stream is None:
            return

        try:
            self.stream.close()
        finally:
            self.status = status.CLOSED
            self.stream = None

    def on_closed_stream(self):
        if self.status != status.CLOSED:
            if self.on_disconnect:
                try:
                    self.on_disconnect()
                except Exception:
                    logger.error('ERROR in on_disconnect() callback',
                                                                 exc_info=True)

    def reset(self):
        for c in self.channels.values():
            if c is not self:
                c.reset()
        super(Connection, self).reset()
        self.close_stream()
