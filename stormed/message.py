from stormed.util import WithFields
from stormed.method import basic

class Message(WithFields):

    _fields = basic.properties

    def __init__(self, body, **properties):
        self.body = body
        self.encoded_body = body.encode('utf8')
        properties.setdefault('content_type', 'application/octet-stream')
        super(Message, self).__init__(**properties)

