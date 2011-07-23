#! /usr/bin/env python

import logging
from tornado.ioloop import IOLoop
from stormed import Connection, Message

ch = None

def on_connect():
    global ch
    ch = conn.channel()
    ch.exchange_declare(exchange='logs', type='fanout')
    ch.queue_declare(exclusive=True, callback=with_temp_queue)

def with_temp_queue(qinfo):
    ch.queue_bind(exchange='logs', queue=qinfo.queue)
    ch.consume(qinfo.queue, callback, no_ack=True)

def callback(msg):
    print " [x] %r" % msg.body

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
print ' [*] Waiting for logs. To exit press CTRL+C'
try:
    io_loop.start()
except KeyboardInterrupt:
    conn.close(io_loop.stop)
