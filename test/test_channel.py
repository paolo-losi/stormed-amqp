import unittest

from tornado import testing

from stormed.connection import Connection

class TestChannel(testing.AsyncTestCase):

    def test_open(self):
        conn = Connection('localhost', io_loop=self.io_loop)

        def clean_up():
            conn.close(self.stop)
    
        def on_connect():
            ch = conn.channel()
            ch.exchange_declare(name='test', durable=True)
            ch.on_tasks_completed = clean_up

        conn.connect(on_connect)
        self.wait()

if __name__ == '__main__':
    unittest.main()
