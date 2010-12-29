
from stormed.util import WithFields

class Start(WithFields):

    _name      = "connection.start"
    _class_id  = 10
    _method_id = 10
    _fields    = [
        ('version_major'     , 'octet'),
        ('version_minor'     , 'octet'),
        ('server_properties' , 'table'),
        ('mechanisms'        , 'longstr'),
        ('locales'           , 'longstr'),
    ]

class StartOk(WithFields):

    _name      = "connection.start-ok"
    _class_id  = 10
    _method_id = 11
    _fields    = [
        ('client_properties' , 'table'),
        ('mechanism'         , 'shortstr'),
        ('response'          , 'longstr'),
        ('locale'            , 'shortstr'),
    ]

class Secure(WithFields):

    _name      = "connection.secure"
    _class_id  = 10
    _method_id = 20
    _fields    = [
        ('challenge'         , 'longstr'),
    ]

class SecureOk(WithFields):

    _name      = "connection.secure-ok"
    _class_id  = 10
    _method_id = 21
    _fields    = [
        ('response'          , 'longstr'),
    ]

class Tune(WithFields):

    _name      = "connection.tune"
    _class_id  = 10
    _method_id = 30
    _fields    = [
        ('channel_max'       , 'short'),
        ('frame_max'         , 'long'),
        ('heartbeat'         , 'short'),
    ]

class TuneOk(WithFields):

    _name      = "connection.tune-ok"
    _class_id  = 10
    _method_id = 31
    _fields    = [
        ('channel_max'       , 'short'),
        ('frame_max'         , 'long'),
        ('heartbeat'         , 'short'),
    ]

class Open(WithFields):

    _name      = "connection.open"
    _class_id  = 10
    _method_id = 40
    _fields    = [
        ('virtual_host'      , 'shortstr'),
        ('capabilities'      , 'shortstr'),
        ('insist'            , 'bit'),
    ]

class OpenOk(WithFields):

    _name      = "connection.open-ok"
    _class_id  = 10
    _method_id = 41
    _fields    = [
        ('known_hosts'       , 'shortstr'),
    ]

class Close(WithFields):

    _name      = "connection.close"
    _class_id  = 10
    _method_id = 50
    _fields    = [
        ('reply_code'        , 'short'),
        ('reply_text'        , 'shortstr'),
        ('class_id'          , 'short'),
        ('method_id'         , 'short'),
    ]

class CloseOk(WithFields):

    _name      = "connection.close-ok"
    _class_id  = 10
    _method_id = 51
    _fields    = [
    ]


id2method = {
    10: Start,
    11: StartOk,
    20: Secure,
    21: SecureOk,
    30: Tune,
    31: TuneOk,
    40: Open,
    41: OpenOk,
    50: Close,
    51: CloseOk,
}
