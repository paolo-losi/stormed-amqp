#! /usr/bin/env python

import logging
import sys
from tornado.ioloop import IOLoop
from stormed import Connection, Message

# delivery_mode=2 makes message persistent
msg = Message(' '.join(sys.argv[1:]) or 'Hello World!', delivery_mode=2)

def on_connect():
    ch = conn.channel()
    ch.queue_declare(queue='task_queue', durable=True)
    ch.publish(msg, exchange='', routing_key='task_queue')
    conn.close(callback=done)

def done():
    print " [x] Sent %r" % msg.body
    io_loop.stop()

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
io_loop.start()
