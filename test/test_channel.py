import unittest

from tornado import testing

from stormed.connection import Connection
from stormed.channel import Consumer
from stormed.message import Message
from stormed.method import queue
from stormed.frame import status

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

        def on_creation(queue, message_count, consumer_count):
            assert queue == 'test_queue'
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
        ch = None
        test_msg = Message('test')

        def on_msg(msg):
            global ch
            assert msg.body == 'test'
            msg.ack()
            ch.get('test_queue', on_missing_msg)

        def on_missing_msg(msg):
            assert msg is None
            conn.close(self.stop)

        def on_connect():
            global ch
            ch = conn.channel()
            ch.exchange_declare('test_exchange', durable=False)
            ch.queue_declare('test_queue', durable=False)
            ch.queue_bind('test_queue', 'test_exchange', 'test')
            ch.publish(test_msg, exchange='test_exchange', routing_key='test')
            ch.get('test_queue', on_msg)

        conn.connect(on_connect)
        self.wait()

    def test_consume(self):
        global count
        conn = Connection('localhost', io_loop=self.io_loop)
        test_msg = Message('test')
        count = 0

        def clean_up():
            assert not ch.consumers
            conn.close(self.stop)

        def consume_callback(msg):
            global ch, count, consumer
            count += 1
            assert msg.body == 'test'
            if count == 5:
                consumer.cancel(clean_up)

        def on_connect():
            global ch, consumer
            ch = conn.channel()
            ch.exchange_declare('test_exchange', durable=False)
            ch.queue_declare('test_queue', durable=False)
            ch.queue_bind('test_queue', 'test_exchange', 'test')
            for _ in xrange(5):
                ch.publish(test_msg, exchange='test_exchange',
                                     routing_key='test')
            consumer = Consumer(consume_callback)
            ch.consume('test_queue', consumer, no_ack=True)

        conn.connect(on_connect)
        self.wait()

    def test_channel_error(self):
        
        conn = Connection('localhost', io_loop=self.io_loop)

        def on_connect():
            self.ch = conn.channel()
            self.ch.on_error = on_error
            self.ch.queue_bind('foo', 'bar')

        def on_error(ch_error):
            assert ch_error.method == queue.Bind, ch_error.method
            assert ch_error.reply_code == 'NOT_FOUND'
            assert self.ch.status == status.CLOSED
            conn.close(self.stop)

        conn.connect(on_connect)
        self.wait()

if __name__ == '__main__':
    unittest.main()
