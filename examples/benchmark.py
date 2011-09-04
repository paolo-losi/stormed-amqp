#!/usr/bin/env python

from tornado import ioloop, web, httpserver
from stormed import Message, Connection

"""
RoundTrip benchmark.
For each single request:
1. publish is own id on the broker
2. the broker replies with the id
3. the request is "finished"

1. Run this example
2. ab -n 1000 -c 10 http://localhost:8001/round_trip
"""

XNAME = "tornado_test_exchage"
QNAME = "tornado_test_queue"


request_map = dict()

def finish_request(msg):
    req_id = msg.body
    request = request_map.pop(req_id)
    request.write(req_id)
    request.finish()


class RoundTripHandler(web.RequestHandler):

    @web.asynchronous
    def get(self):
        req_id = str(id(self))
        request_map[req_id] = self
        msg = Message(req_id, delivery_mode=1)
        ch.publish(msg, exchange=XNAME)


def on_amqp_connection():
    global ch
    ch = conn.channel()
    ch.exchange_declare(exchange=XNAME, type="fanout")
    ch.queue_declare(queue=QNAME, durable=False)
    ch.queue_bind(queue=QNAME, exchange=XNAME)
    ch.consume(QNAME, finish_request, no_ack=True)

    application = web.Application([
        (r"/round_trip", RoundTripHandler),
    ])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(8001)

ch = None
conn = None

def main():
    global ch, conn
    conn = Connection(host='localhost')
    conn.connect(on_amqp_connection)

    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        conn.close()
