#!/usr/bin/env python

import logging
from tornado.ioloop import IOLoop
from stormed import Connection, Message

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_connect():
    global ch
    ch = conn.channel()
    ch.queue_declare(queue='rpc_queue', durable=True)
    ch.qos(prefetch_count=1)
    ch.consume('rpc_queue', on_request)

def on_request(msg):
    n = int(msg.body)
    print " [.] fib(%s)" % n
    response = str(fib(n))
    response_msg = Message(response, delivery_mode=2,
                           correlation_id=msg.correlation_id)
    ch.publish(response_msg, exchange='', routing_key=msg.reply_to)
    msg.ack()

logging.basicConfig()
ch = None
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
print ' [*] Waiting for messages. To exit press CTRL+C'
try:
    io_loop.start()
except KeyboardInterrupt:
    conn.close(io_loop.stop)
