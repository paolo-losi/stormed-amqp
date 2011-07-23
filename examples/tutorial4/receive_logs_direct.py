#! /usr/bin/env python

import logging
import sys
from tornado.ioloop import IOLoop
from stormed import Connection, Message

severities = sys.argv[1:]
if not severities:
    print >> sys.stderr, "Usage: %s [info] [warning] [error]" % sys.argv[0]
    sys.exit(1)

ch = None

def on_connect():
    global ch
    ch = conn.channel()
    ch.exchange_declare(exchange='direct_logs', type='direct')
    ch.queue_declare(exclusive=True, callback=with_temp_queue)

def with_temp_queue(qinfo):
    for severity in severities:
        ch.queue_bind(exchange='direct_logs',
                      queue=qinfo.queue,
                      routing_key=severity)
    ch.consume(qinfo.queue, callback, no_ack=True)

def callback(msg):
    print " [x] %r:%r" % (msg.rx_data.routing_key, msg.body)

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
print ' [*] Waiting for logs. To exit press CTRL+C'
try:
    io_loop.start()
except KeyboardInterrupt:
    conn.close(io_loop.stop)
