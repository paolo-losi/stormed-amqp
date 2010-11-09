import socket
from tornado.iostream import IOStream
from tornado.ioloop import IOLoop
from tornado import stack_context

from stormed.util import Enum
from stormed.frame import FrameReader
from stormed import frame
from stormed.serialization import parse_method, table2str
from stormed.method.connection import StartOk, TuneOk, Open, Close

status = Enum('HANDSHAKE', 'CONNECTED', 'CLOSED', 'CLOSING')

class Connection(object):

    def __init__(self, host, username='guest', password='guest', vhost='/',
                       port=5672, io_loop=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost
        self.io_loop = io_loop or IOLoop.instance()
        self.stream = None
        self.on_connect_callback = None
        self.on_close_callback = None
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
        if frame.frame_type == 'method':
            self.handle_method(frame)
        if self.stream is not None:
            FrameReader(self.stream, self._frame_loop)

    def write_method(self, method, channel=0):
        f = frame.from_method(method, channel)
        self.stream.write(f)

    def handle_method(self, method_frame):
        method = method_frame.payload
        if method.name == 'connection.start':
            #FIXME handle missing PLAIN mechanism
            assert 'AMQPLAIN' in method.mechanisms.split(' ')
            assert 'en_US' in method.locales.split(' ')
            response = table2str(dict(LOGIN    = self.username,
                                      PASSWORD = self.password))
            #TODO more peer_properties
            start_ok = StartOk(peer_properties=dict(client="stormed-amqp"),
                               mechanism='AMQPLAIN', response=response,
                               locale='en_US')
            self.write_method(start_ok)
        elif method.name == 'connection.tune':
            tune_ok = TuneOk(frame_max=method.frame_max,
                             channel_max=method.channel_max,
                             hearbeat=method.hearbeat)
            self.write_method(tune_ok)
            _open = Open(virtual_host=self.vhost, capabilities='', insist=0)
            self.write_method(_open)
        elif method.name == 'connection.open-ok':
            self.status = status.CONNECTED
            self.on_connect_callback()
        elif method.name == 'connection.close-ok':
            self.stream.close()
            self.stream = None
            self.status = status.CLOSED
            self.on_close_callback()
        else:
            #FIXME log errore
            print "ERROR", method

    def close(self, callback):
        _close = Close(reply_code=0, reply_text='', _class_id=0, _method_id=0)
        self.write_method(_close)
        self.status = status.CLOSING
        self.on_close_callback = stack_context.wrap(callback)
