from stormed.util import add_method
from stormed.method.codegen.basic import *

@add_method(GetOk)
def handle(self, ch):
    ch.invoke_callback(ch.message)

@add_method(GetEmpty)
def handle(self, ch):
    ch.invoke_callback(None)
