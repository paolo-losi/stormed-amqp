from stormed.util import add_method, Enum
from stormed.serialization import table2str
from stormed.frame import status
from stormed.method.codegen.channel import *
from stormed.method.codegen import id2class
from stormed.method.constant import id2constant

@add_method(OpenOk)
def handle(self, channel):
    channel.status = status.OPENED

@add_method(CloseOk)
def handle(self, channel):
    channel.status = status.CLOSED

class ChannelError(object):

    def __init__(self, reply_code, reply_text, method):
        self.reply_code = reply_code
        self.reply_text = reply_text
        self.method = method

@add_method(Close)
def handle(self, channel):
    try:
        mod = id2class[self.class_id]
        method = getattr(mod, 'id2method')[self.method_id]
    except:
        method = None
        raise
    channel.hard_reset()
    error_code = id2constant.get(self.reply_code, '')
    if channel.on_error:
        channel.on_error(ChannelError(error_code, self.reply_text, method)) 
