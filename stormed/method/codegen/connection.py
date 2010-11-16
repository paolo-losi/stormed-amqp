
from stormed.util import WithFields

class Start(WithFields):

    _name      = "connection.start"
    _class_id  = 10
    _method_id = 10
    _fields    = [
        (u'version_major'    , u'octet'),
        (u'version_minor'    , u'octet'),
        (u'server_properties', u'table'),
        (u'mechanisms'       , u'longstr'),
        (u'locales'          , u'longstr'),
    ]

class StartOk(WithFields):

    _name      = "connection.start-ok"
    _class_id  = 10
    _method_id = 11
    _fields    = [
        (u'client_properties', u'table'),
        (u'mechanism'        , u'shortstr'),
        (u'response'         , u'longstr'),
        (u'locale'           , u'shortstr'),
    ]

class Secure(WithFields):

    _name      = "connection.secure"
    _class_id  = 10
    _method_id = 20
    _fields    = [
        (u'challenge'        , u'longstr'),
    ]

class SecureOk(WithFields):

    _name      = "connection.secure-ok"
    _class_id  = 10
    _method_id = 21
    _fields    = [
        (u'response'         , u'longstr'),
    ]

class Tune(WithFields):

    _name      = "connection.tune"
    _class_id  = 10
    _method_id = 30
    _fields    = [
        (u'channel_max'      , u'short'),
        (u'frame_max'        , u'long'),
        (u'heartbeat'        , u'short'),
    ]

class TuneOk(WithFields):

    _name      = "connection.tune-ok"
    _class_id  = 10
    _method_id = 31
    _fields    = [
        (u'channel_max'      , u'short'),
        (u'frame_max'        , u'long'),
        (u'heartbeat'        , u'short'),
    ]

class Open(WithFields):

    _name      = "connection.open"
    _class_id  = 10
    _method_id = 40
    _fields    = [
        (u'virtual_host'     , u'shortstr'),
        (u'capabilities'     , u'shortstr'),
        (u'insist'           , u'bit'),
    ]

class OpenOk(WithFields):

    _name      = "connection.open-ok"
    _class_id  = 10
    _method_id = 41
    _fields    = [
        (u'known_hosts'      , u'shortstr'),
    ]

class Close(WithFields):

    _name      = "connection.close"
    _class_id  = 10
    _method_id = 50
    _fields    = [
        (u'reply_code'       , u'short'),
        (u'reply_text'       , u'shortstr'),
        (u'class_id'         , u'short'),
        (u'method_id'        , u'short'),
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
