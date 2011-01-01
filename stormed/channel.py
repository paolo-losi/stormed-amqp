from stormed.util import Enum
from stormed.method.channel import Open, Close, status
from stormed.method import exchange as _exchange, basic, queue as _queue
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

    def exchange_declare(self, exchange, type="direct", durable=False,
                               callback=None):
        self.send_method(_exchange.Declare(ticket      = 0,
                                           exchange    = exchange,
                                           type        = type,
                                           passive     = False,
                                           durable     = durable,
                                           auto_delete = False,
                                           internal    = False,
                                           nowait      = False,
                                           arguments   = dict()), callback)

    def exchange_delete(self, exchange, if_unused=False, callback=None):
        self.send_method(_exchange.Delete(ticket    = 0,
                                          exchange  = exchange,
                                          if_unused = if_unused,
                                          nowait    = False), callback)

    def queue_declare(self, queue, passive=False, durable=True, exclusive=False,
                            auto_delete=False, callback=None):
        self.send_method(_queue.Declare(ticket      = 0,
                                        queue       = queue,
                                        passive     = passive,
                                        durable     = durable,
                                        exclusive   = exclusive,
                                        auto_delete = auto_delete,
                                        nowait      = False,
                                        arguments   = dict()), callback)

    def queue_delete(self, queue, if_unused=False, if_empty=False,
                           callback=None):
        self.send_method(_queue.Delete(ticket    = 0,
                                       queue     = queue,
                                       if_unused = if_unused,
                                       if_empty  = if_empty,
                                       nowait    = False), callback)

    def queue_bind(self, queue, exchange, routing_key='', callback=None):
        self.send_method(_queue.Bind(ticket      = 0,
                                     queue       = queue,
                                     exchange    = exchange,
                                     routing_key = routing_key,
                                     nowait      = False,
                                     arguments   = dict()), callback)
                                            
    def publish(self, message, exchange, routing_key='', immediate=False,
                      mandatory=False):
        self.send_method(basic.Publish(ticket = 0,
                                       exchange = exchange,
                                       routing_key = routing_key,
                                       mandatory = mandatory,
                                       immediate = immediate), message=message)

    def get(self, queue, callback, no_ack=False):
        _get = basic.Get(ticket=0, queue=queue, no_ack=no_ack)
        self.send_method(_get, callback)
