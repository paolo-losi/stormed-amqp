from stormed.util import add_method
from stormed.method.codegen.basic import *

@add_method(GetOk)
def handle(self, ch):
    msg = ch.message
    msg.rx_channel = ch
    ch.invoke_callback(msg)

@add_method(GetEmpty)
def handle(self, ch):
    ch.invoke_callback(None)
