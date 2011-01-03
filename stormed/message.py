from stormed.util import WithFields
from stormed.method import basic

class Message(WithFields):

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
        if self.rx_channel is None:
            raise ValueError('cannot ack an unreceived message')
        method = basic.Ack(delivery_tag=self.rx_data.delivery_tag,
                           multiple=multiple)
        self.rx_channel.send_method(method)

    def reject(self, requeue=True):
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
