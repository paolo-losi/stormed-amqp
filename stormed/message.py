from stormed.util import WithFields
from stormed.method import basic

class Message(WithFields):

    """An AMQP Message

    The body parameter represents the message content. If the parameter
    is a unicode object, it is encoded to UTF8.

    The optional properties are those defined in the AMQP standard
    (see stormed.method.codegen.basic.properties)

    When the message is received from the server the rx_data attribute
    contains the AMQP method instance (e.g. basic.GetOk, basic.Deliver).
    This instance carries the server metadata (e.g. the redelivered bit).

    A message received from the server can be acknowledged o rejected
    with the Message.ack() and Message.reject() methods if required.
    """

    _fields = basic.properties

    def __init__(self, body, **properties):
        self.body = body
        if isinstance(body, unicode):
            encoding = properties.setdefault('content_encoding', 'utf8')
            self.body = body.encode(encoding)
        else:
            properties.setdefault('content_type', 'application/octet-stream')
        self.rx_data = None
        self.rx_channel = None
        super(Message, self).__init__(**properties)

    def ack(self, multiple=False):
        """acknowledge the message"""
        if self.rx_channel is None:
            raise ValueError('cannot ack an unreceived message')
        method = basic.Ack(delivery_tag=self.rx_data.delivery_tag,
                           multiple=multiple)
        self.rx_channel.send_method(method)

    def nack(self, multiple=False, requeue=True):
        """reject the message"""
        if self.rx_channel is None:
            raise ValueError('cannot nack an unreceived message')
        method = basic.Nack(delivery_tag=self.rx_data.delivery_tag,
                            multiple=multiple, requeue=requeue)
        self.rx_channel.send_method(method)

    def reject(self, requeue=True):
        """reject the message"""
        if self.rx_channel is None:
            raise ValueError('cannot reject an unreceived message')
        method = basic.Reject(delivery_tag=self.rx_data.delivery_tag,
                              requeue=requeue)
        self.rx_channel.send_method(method)


class ContentHeader(object):

    def __init__(self, size, properties):
        self.size = size
        self.properties = properties


class MessageBuilder(object):

    def __init__(self, content_method):
        self.content_method = content_method
        self.content_header = None
        self.chunks = []
        self.received_size = 0

    def add_content_header(self, content_header):
        self.content_header = content_header

    def add_content_body(self, content_body):
        self.chunks.append(content_body)
        self.received_size += len(content_body)

    @property
    def msg_complete(self):
        return self.content_header.size == self.received_size

    def get_msg(self):
        assert self.msg_complete
        body = ''.join(self.chunks)
        msg = Message(body, **self.content_header.properties)
        msg.rx_data = self.content_method
        return msg
