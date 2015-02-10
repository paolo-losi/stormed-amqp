from stormed.util import add_method, AmqpError, logger
from stormed.serialization import table2str
from stormed.heartbeat import HeartbeatMonitor
from stormed.frame import status
from stormed.method.codegen import id2class
from stormed.method.constant import id2constant
from stormed.method.codegen.connection import *

@add_method(Start)
def handle(self, conn):
    if 'AMQPLAIN' not in self.mechanisms.split(' '):
        raise AmqpError("'AMQPLAIN' not in mechanisms")
    if 'en_US' not in self.locales.split(' '):
        raise AmqpError("'en_US' not in locales")
    response = table2str(dict(LOGIN    = conn.username,
                              PASSWORD = conn.password))
    client_properties = {'client': 'stormed-amqp'}

    start_ok = StartOk(client_properties=client_properties,
                       mechanism='AMQPLAIN', response=response,
                       locale='en_US')
    conn.write_method(start_ok)

@add_method(Tune)
def handle(self, conn):
    conn.frame_max = self.frame_max or 2**16
    tune_ok = TuneOk(frame_max   = conn.frame_max,
                     channel_max = self.channel_max,
                     heartbeat   = conn.heartbeat)
    conn.write_method(tune_ok)
    _open = Open(virtual_host = conn.vhost,
                 capabilities = '',
                 insist       = 0)
    conn.write_method(_open)

@add_method(OpenOk)
def handle(self, conn):
    conn.status = status.OPENED
    if conn.heartbeat:
        HeartbeatMonitor(conn).start()
    try:
        conn.on_connect()
    except Exception:
        logger.error('ERROR in on_connect() callback', exc_info=True)

@add_method(CloseOk)
def handle(self, conn):
    conn.status = status.CLOSED
    conn.invoke_callback()
    conn.reset()

class ConnectionError(object):

    def __init__(self, reply_code, reply_text, method):
        self.reply_code = reply_code
        self.reply_text = reply_text
        self.method = method

@add_method(Close)
def handle(self, conn):
    try:
        mod = id2class[self.class_id]
        method = getattr(mod, 'id2method')[self.method_id]
    except:
        method = None
    conn.reset()
    error_code = id2constant.get(self.reply_code, '')
    logger.warn('Connection Hard Error. code=%r. %s', error_code,
                                                      self.reply_text)
    if conn.on_error:
        try:
            conn.on_error(ConnectionError(error_code, self.reply_text, method))
        except Exception:
            logger.error('ERROR in on_error() callback', exc_info=True)
