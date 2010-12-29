from stormed.util import add_method, Enum
from stormed.serialization import table2str
from stormed.method.codegen.channel import *

status = Enum('OPENING', 'OPENED', 'CLOSED', 'CLOSING')

@add_method(OpenOk)
def handle(self, channel):
    channel.status = status.OPENED

@add_method(CloseOk)
def handle(self, channel):
    channel.status = status.CLOSED
