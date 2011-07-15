#! /usr/bin/env python

import logging
from tornado.ioloop import IOLoop
from stormed import Connection, Message

def on_connect():
    ch = conn.channel()
    ch.queue_declare(queue='hello')
    ch.consume('hello', callback, no_ack=True)

def callback(msg):
    print " [x] Received %r" % msg.body

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
print ' [*] Waiting for messages. To exit press CTRL+C'
try:
    io_loop.start()
except KeyboardInterrupt:
    conn.close(io_loop.stop)
