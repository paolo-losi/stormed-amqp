from stormed.util import add_method, Enum, logger
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
    del channel.conn.channels[channel.channel_id]
    channel.invoke_callback()
    channel.conn = None
    channel.reset()

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
    channel.reset()
    error_code = id2constant.get(self.reply_code, '')
    logger.warn('Soft Error. channel=%r code=%r. %s', channel.channel_id,
                                                      error_code,
                                                      self.reply_text)
    if channel.on_error:
        try:
            channel.on_error(ChannelError(error_code, self.reply_text, method))
        except Exception:
            logger.error('ERROR in on_error() callback for channel %d',
                                             channel.channel_id, exc_info=True)

@add_method(Flow)
def handle(self, channel):
    channel.flow_stopped = not self.active
    self.send_method(FlowOk(active=self.active))
