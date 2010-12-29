from stormed.util import Enum
from stormed.method.channel import Open, status
from stormed.method import exchange, basic

class Channel(object):

    def __init__(self, channel_id, conn):
        self.channel_id = channel_id
        self.conn = conn
        self.status = status.CLOSED
        self._reply_queue = []

    def open(self, callback=None):
        self._send_method(Open(out_of_band=''), callback)

    def exchange_declare(self, name, type="direct", durable=False,
                               callback=None):
        self._send_method(exchange.Declare(ticket      = 0,
                                           exchange    = name,
                                           type        = type,
                                           passive     = False,
                                           durable     = durable,
                                           auto_delete = False,
                                           internal    = False,
                                           nowait      = False,
                                           arguments   = dict()), callback)

    def publish(self, message, exchange, routing_key, immediate=False,
                      mandatory=False, callback=None):
        self._send_method(basic.Publish(ticket = 0,
                                        exchange = exchange,
                                        routing_key = routing_key,
                                        mandatory = mandatory,
                                        immediate = immediate), callback)
        self.conn.write_msg(message, channel=self.channel_id)

    #TODO do we need FrameHandler class?
    def handle_frame(self, frame):
        method = frame.payload
        if hasattr(method, 'handle'):
            method.handle(self)
            #FIXME verify if the answer is the one we're expecting
            method, callback = self._reply_queue.pop(0)
            if callback is not None:
                callback()
        else:
            #TODO better error reporting/handling
            print "ERROR: %r not handled" % method._name

    def _send_method(self, method, callback):
        self._reply_queue.append( (method, callback) )
        self.conn.write_method(method, channel=self.channel_id)
