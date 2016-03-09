#! /usr/bin/env python

import logging
from tornado.ioloop import IOLoop
from stormed import Connection


def on_connect():
    ch = conn.channel()
    ch.queue_declare(queue='hello')
    ch.consume('hello', callback, no_ack=True)


def callback(msg):
    print "[x] Received %r" % msg.body


def on_close():
    print "[*] reconnecting ..."
    conn.connect(on_connect, on_close)

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect, on_close)
io_loop = IOLoop.instance()
print ' [*] Waiting for messages. To exit press CTRL+C'
try:
    io_loop.start()
except KeyboardInterrupt:
    conn.close(io_loop.stop)
