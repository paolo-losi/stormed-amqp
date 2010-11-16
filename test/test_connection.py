import unittest

from tornado import testing

from stormed.connection import Connection, status

class TestConnectionHandshake(testing.AsyncTestCase):

    def test_handshake(self):
        conn = Connection('localhost', io_loop=self.io_loop)
        def on_connect():
            self.assertEquals(conn.status, status.CONNECTED)
            conn.close(self.stop)
        conn.connect(on_connect)
        self.wait()

if __name__ == '__main__':
    unittest.main()
