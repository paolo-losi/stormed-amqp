#! /usr/bin/env python

import logging
import sys
from tornado.ioloop import IOLoop
from stormed import Connection, Message

# delivery_mode=2 makes message persistent
routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
msg = Message(' '.join(sys.argv[2:]) or 'Hello World!')

def on_connect():
    ch = conn.channel()
    ch.exchange_declare(exchange='topic_logs', type='topic')
    ch.publish(msg, exchange='topic_logs', routing_key=routing_key)
    conn.close(callback=done)

def done():
    print " [x] Sent %r:%r" % (routing_key, msg.body)
    io_loop.stop()

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
io_loop.start()
