#!/usr/bin/env python

import logging
import sys
import uuid
from tornado.ioloop import IOLoop
from stormed import Connection, Message

class FibonacciRpcClient(object):
    def __init__(self, n):
        self.conn = Connection(host='localhost')
        self.conn.connect(self.on_connect)
        self.n = n
    
    def on_connect(self):
        self.ch = self.conn.channel()
        self.ch.queue_declare(exclusive=True, callback=self.on_queue_declare)
    
    def on_queue_declare(self, q_info):
        callback_queue = q_info.queue
        self.ch.consume(callback_queue, self.on_response)
        self.corr_id = str(uuid.uuid4())
        msg = Message(str(self.n), delivery_mode=2, reply_to=callback_queue,
                      correlation_id=self.corr_id)
        self.ch.publish(msg, exchange='', routing_key='rpc_queue')
    
    def on_response(self, msg):
        if self.corr_id == msg.correlation_id:
            print " [x] Received %r" % msg.body
            self.conn.close(callback=IOLoop.instance().stop)
            print 'Closing connection.'

logging.basicConfig()
try:
    n = int(sys.argv[1])
except:
    n = 30
io_loop = IOLoop.instance()
fibonacci_rpc = FibonacciRpcClient(n)
print ' [x] Requesting fib(%s)' % n
try:
    io_loop.start()
except:
    io_loop.stop()
