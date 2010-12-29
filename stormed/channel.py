from stormed.util import Enum
from stormed.method.channel import Open, Close, status
from stormed.method import exchange, basic
from stormed.frame import FrameHandler

class Channel(FrameHandler):

    def __init__(self, channel_id, conn):
        self.channel_id = channel_id
        self.status = status.CLOSED #FIXME is it needed?
        super(Channel, self).__init__(conn)

    def open(self, callback=None):
        self.status = status.OPENING
        self.send_method(Open(out_of_band=''), callback)

    def close(self, callback=None):
        self.status = status.CLOSING
        _close = Close(reply_code=0, reply_text='', class_id=0, method_id=0)
        self.send_method(_close, callback)

    def exchange_declare(self, name, type="direct", durable=False,
                               callback=None):
        self.send_method(exchange.Declare(ticket      = 0,
                                          exchange    = name,
                                          type        = type,
                                          passive     = False,
                                          durable     = durable,
                                          auto_delete = False,
                                          internal    = False,
                                          nowait      = False,
                                          arguments   = dict()), callback)

    def publish(self, message, exchange, routing_key, immediate=False,
                      mandatory=False):
        self.send_method(basic.Publish(ticket = 0,
                                       exchange = exchange,
                                       routing_key = routing_key,
                                       mandatory = mandatory,
                                       immediate = immediate), message=message)
