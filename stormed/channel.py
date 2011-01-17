from stormed.util import Enum, AmqpError
from stormed.method.channel import Open, Close, Flow
from stormed.method import exchange as _exchange, basic, queue as _queue, tx
from stormed.frame import FrameHandler, status

class FlowStoppedException(AmqpError): pass

class Channel(FrameHandler):

    def __init__(self, channel_id, conn):
        self.channel_id = channel_id
        self.consumers = {}
        self.status = status.CLOSED
        self.on_error = None
        self.on_return = None
        self.flow_stopped = False
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

    def queue_declare(self, queue='', passive=False, durable=True,
                            exclusive=False, auto_delete=False, callback=None):
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

    def queue_unbind(self, queue, exchange, routing_key='', callback=None):
        self.send_method(_queue.Unind(ticket      = 0,
                                      queue       = queue,
                                      exchange    = exchange,
                                      routing_key = routing_key,
                                      nowait      = False,
                                      arguments   = dict()), callback)

    def queue_purge(self, queue, callback=None):
        self.send_method(_queue.Purge(ticket=0, queue=queue, nowait=False),
                         callback)

    def qos(self, prefetch_size=0, prefetch_count=0, _global=False,
                  callback=None):
        self.send_method(basic.Qos(prefetch_size  = prefetch_size,
                                   prefetch_count = prefetch_count,
                                   _global        = _global), callback)

    def publish(self, message, exchange, routing_key='', immediate=False,
                      mandatory=False):
        if self.flow_stopped:
            raise FlowStoppedException
        if (immediate or mandatory) and self.on_return is None:
            raise AmqpError("on_return callback must be set for "
                            "immediate or mandatory publishing")
        self.send_method(basic.Publish(ticket = 0,
                                       exchange = exchange,
                                       routing_key = routing_key,
                                       mandatory = mandatory,
                                       immediate = immediate), message=message)

    def get(self, queue, callback, no_ack=False):
        _get = basic.Get(ticket=0, queue=queue, no_ack=no_ack)
        self.send_method(_get, callback)

    def consume(self, queue, consumer, no_local=False, no_ack=False,
                      exclusive=False):
        if not isinstance(consumer, Consumer):
            consumer = Consumer(consumer)
        def set_consumer(consumer_tag):
            consumer.tag = consumer_tag
            consumer.channel = self
            self.consumers[consumer_tag] = consumer
        _consume = basic.Consume(ticket       = 0,
                                 queue        = queue,
                                 consumer_tag = '',
                                 no_local     = no_local,
                                 no_ack       = no_ack,
                                 exclusive    = exclusive,
                                 nowait       = False,
                                 arguments    = dict())
        self.send_method(_consume, set_consumer)

    def recover(self, requeue=False, callback=None):
        self.send_method(basic.Recover(requeue=requeue), callback)

    def flow(self, active, callback=None):
        self.send_method(Flow(active=active), callback)

    def select(self, callback=None):
        if self.on_error is None:
            raise AmqpError("Channel.on_error callback must be set for tx mode")
        self.send_method(tx.Select(), callback)

    def commit(self, callback=None):
        self.send_method(tx.Commit(), callback)

    def rollback(self, callback=None):
        self.send_method(tx.Rollback(), callback)

class Consumer(object):

    def __init__(self, callback):
        self.tag = None
        self.channel = None
        self.callback = callback

    def cancel(self, callback):
        _cancel = basic.Cancel(consumer_tag=self.tag, nowait=False)
        self.channel.send_method(_cancel, callback)
