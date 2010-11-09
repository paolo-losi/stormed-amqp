import unittest

from tornado import testing

from stormed.connection import Connection

class TestConnectionHandshake(testing.AsyncTestCase):

    def test_handshake(self):
        conn = Connection('localhost', io_loop=self.io_loop)
        conn.connect(self.stop)
        self.wait()

if __name__ == '__main__':
    unittest.main()
