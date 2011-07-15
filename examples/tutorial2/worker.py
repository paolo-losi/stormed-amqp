#! /usr/bin/env python

import logging
import time
from tornado.ioloop import IOLoop
from stormed import Connection, Message

def on_connect():
    ch = conn.channel()
    ch.queue_declare(queue='task_queue', durable=True)
    ch.qos(prefetch_count=1)
    ch.consume('task_queue', callback)

def callback(msg):
    print " [x] Received %r" % msg.body
    sleep_time = msg.body.count('.')
    io_loop.add_timeout(time.time() + sleep_time, lambda: done(msg))

def done(msg):
    print " [x] Done"
    msg.ack()

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
print ' [*] Waiting for messages. To exit press CTRL+C'
try:
    io_loop.start()
except KeyboardInterrupt:
    conn.close(io_loop.stop)
