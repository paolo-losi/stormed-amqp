#! /usr/bin/env python

from tornado.ioloop import IOLoop, PeriodicCallback
from stormed import Connection, Message

msg = Message('Hello World!')


def on_connect():
    ch = conn.channel()
    ch.queue_declare(queue='hello')

    def _send():
        ch.publish(msg, exchange='', routing_key='hello')
        print '[*] Message sent'

    cb = PeriodicCallback(_send, 1000)
    cb.start()

conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
io_loop.start()
