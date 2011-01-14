from stormed.util import add_method
from stormed.method.codegen.queue import *

@add_method(DeclareOk)
def handle(self, ch):
    if ch.callback:
        ch.invoke_callback(self)

@add_method(PurgeOk)
def handle(self, channel):
    channel.invoke_callback(self.message_count)
