import unittest

from tornado import testing

from stormed.connection import Connection
from stormed.message import Message

class TestChannel(testing.AsyncTestCase):

    def test_open(self):
        conn = Connection('localhost', io_loop=self.io_loop)

        def clean_up(**kargs):
            conn.close(self.stop)
    
        def on_connect():
            ch = conn.channel(callback=clean_up)

        conn.connect(on_connect)
        self.wait()

    def test_publish(self):
        conn = Connection('localhost', io_loop=self.io_loop)
        test_msg = Message('test')

        def clean_up():
            conn.close(self.stop)

        def on_connect():
            ch = conn.channel()
            ch.exchange_declare('test_exchange', durable=False)
            ch.publish(test_msg, exchange='test_exchange', routing_key='test')
            ch.close(clean_up)

        conn.connect(on_connect)
        self.wait()

    def test_queue(self):
        conn = Connection('localhost', io_loop=self.io_loop)

        def clean_up():
            conn.close(self.stop)

        def on_creation(message_count, consumer_count):
            assert message_count == 0
            assert consumer_count == 0

        def on_connect():
            ch = conn.channel()
            ch.queue_delete('test_queue')
            ch.queue_declare('test_queue', durable=False,
                             callback=on_creation)
            ch.close(clean_up)

        conn.connect(on_connect)
        self.wait()

    def test_get(self):
        conn = Connection('localhost', io_loop=self.io_loop)
        test_msg = Message('test')

        def on_msg(msg):
            assert msg.body == 'test'
            conn.close(self.stop)

        def on_connect():
            ch = conn.channel()
            ch.exchange_declare('test_exchange', durable=False)
            ch.queue_declare('test_queue', durable=False)
            ch.queue_bind('test_queue', 'test_exchange', 'test')
            ch.publish(test_msg, exchange='test_exchange', routing_key='test')
            ch.get('test_queue', on_msg)

        conn.connect(on_connect)
        self.wait()


if __name__ == '__main__':
    unittest.main()
