import unittest

from tornado import testing

from stormed.connection import Connection
from stormed.message import Message

class TestChannel(testing.AsyncTestCase):

    def test_open(self):
        conn = Connection('localhost', io_loop=self.io_loop)

        def clean_up():
            conn.close(self.stop)
    
        def on_connect():
            ch = conn.channel(callback=clean_up)
            ch.exchange_declare(name='test', durable=True, callback=clean_up)

        conn.connect(on_connect)
        self.wait()

    def test_publish(self):
        conn = Connection('localhost', io_loop=self.io_loop)
        test_msg = Message('test')

        def on_connect():
            ch = conn.channel()
            ch.exchange_declare(name='test', durable=True)
            ch.publish(test_msg, exchange='test', routing_key='test')
            conn.close(self.stop)

        conn.connect(on_connect)
        self.wait()

if __name__ == '__main__':
    unittest.main()
