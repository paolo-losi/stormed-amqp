from stormed.method.codegen import connection
from stormed.method.codegen import channel
from stormed.method.codegen import access
from stormed.method.codegen import exchange
from stormed.method.codegen import queue
from stormed.method.codegen import basic
from stormed.method.codegen import tx
from stormed.method.codegen import confirm

id2class = {
    10: connection,
    20: channel,
    30: access,
    40: exchange,
    50: queue,
    60: basic,
    90: tx,
    85: confirm,
}
