#! /usr/bin/env python

import logging
import sys
from tornado.ioloop import IOLoop
from stormed import Connection, Message

# delivery_mode=2 makes message persistent
msg = Message(' '.join(sys.argv[1:]) or 'info: Hello World!')

def on_connect():
    ch = conn.channel()
    ch.exchange_declare(exchange='logs', type='fanout')
    ch.publish(msg, exchange='logs', routing_key='')
    conn.close(callback=done)

def done():
    print " [x] Sent %r" % msg.body
    io_loop.stop()

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
io_loop.start()
