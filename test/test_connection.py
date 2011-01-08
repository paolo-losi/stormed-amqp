import time
import unittest

from tornado import testing

from stormed.connection import Connection, status
from stormed.method.connection import Tune
from stormed.heartbeat import HeartbeatMonitor

class TestConnectionHandshake(testing.AsyncTestCase):

    def test_handshake(self):
        conn = Connection('localhost', io_loop=self.io_loop)
        def on_connect():
            self.assertEquals(conn.status, status.OPENED)
            conn.close(self.stop)
        conn.connect(on_connect)
        self.wait()

    def test_heartbeat(self):
        conn = Connection('localhost', heartbeat=1, io_loop=self.io_loop)
        def clean_up():
            conn.status == status.OPENED
            conn.close(self.stop)
        conn.connect(lambda: None)
        self.io_loop.add_timeout(time.time()+4, clean_up)
        self.wait()

    def test_heartbeat_server_disconnected(self):
        conn = Connection('localhost', io_loop=self.io_loop)
        def clean_up():
            conn.status == status.CLOSED
            self.stop()
        conn.on_disconnect = clean_up

        def launch_heartbeat():
            conn.heartbeat=1
            HeartbeatMonitor(conn).start()
        conn.connect(launch_heartbeat)

        self.io_loop.add_timeout(time.time()+3, clean_up)
        self.wait()

    def test_heartbeat_client_disconnected(self):
        conn = Connection('localhost', heartbeat=1, io_loop=self.io_loop)
        conn.process_heartbeat = lambda hb: None
        conn.on_disconnect = self.stop
        conn.connect(lambda: None)
        self.wait()

    def test_conn_error(self):
        conn = Connection('localhost', io_loop=self.io_loop)

        def send_wrong_method():
            tune = Tune(frame_max   = 0,
                        channel_max = 0,
                        heartbeat   = 0)
            conn.send_method(tune, callback=done)

        def done(conn_error):
            assert conn_error.method == Tune, repr(conn_error.method)
            assert conn_error.reply_code == 'CHANNEL_ERROR'
            assert conn.status == status.CLOSED
            self.stop()

        conn.on_error = done
        conn.connect(send_wrong_method)
        self.wait()
        

if __name__ == '__main__':
    unittest.main()
