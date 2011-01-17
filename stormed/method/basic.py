from stormed.util import add_method, logger
from stormed.method.codegen.basic import *

@add_method(GetOk)
def handle(self, ch):
    msg = ch.message
    msg.rx_channel = ch
    ch.invoke_callback(msg)

@add_method(GetEmpty)
def handle(self, ch):
    ch.invoke_callback(None)

@add_method(ConsumeOk)
def handle(self, ch):
    ch.invoke_callback(self.consumer_tag)

@add_method(CancelOk)
def handle(self, ch):
    del ch.consumers[self.consumer_tag]

@add_method(Deliver)
def handle(self, ch):
    msg = ch.message
    msg.rx_channel = ch
    ch.consumers[self.consumer_tag].callback(msg)

@add_method(Return)
def handle(self, ch):
    msg = ch.message
    msg.rx_channel = ch
    if ch.on_return:
        try:
            ch.on_return(msg)
        except Exception:
            logger.error('ERROR in on_return() callback', exc_info=True)
