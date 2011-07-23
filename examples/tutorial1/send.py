#! /usr/bin/env python

import logging
from tornado.ioloop import IOLoop
from stormed import Connection, Message

msg = Message('Hello World!')

def on_connect():
    ch = conn.channel()
    ch.queue_declare(queue='hello')
    ch.publish(msg, exchange='', routing_key='hello')
    conn.close(callback=done)

def done():
    print " [x] Sent 'Hello World!'"
    io_loop.stop()

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
io_loop.start()
