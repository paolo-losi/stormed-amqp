
from stormed.util import WithFields

class Open(WithFields):

    _name      = "channel.open"
    _class_id  = 20
    _method_id = 10
    _fields    = [
        ('out_of_band'       , 'shortstr'),
    ]

class OpenOk(WithFields):

    _name      = "channel.open-ok"
    _class_id  = 20
    _method_id = 11
    _fields    = [
        ('channel_id'        , 'longstr'),
    ]

class Flow(WithFields):

    _name      = "channel.flow"
    _class_id  = 20
    _method_id = 20
    _fields    = [
        ('active'            , 'bit'),
    ]

class FlowOk(WithFields):

    _name      = "channel.flow-ok"
    _class_id  = 20
    _method_id = 21
    _fields    = [
        ('active'            , 'bit'),
    ]

class Close(WithFields):

    _name      = "channel.close"
    _class_id  = 20
    _method_id = 40
    _fields    = [
        ('reply_code'        , 'short'),
        ('reply_text'        , 'shortstr'),
        ('class_id'          , 'short'),
        ('method_id'         , 'short'),
    ]

class CloseOk(WithFields):

    _name      = "channel.close-ok"
    _class_id  = 20
    _method_id = 41
    _fields    = [
    ]


id2method = {
    10: Open,
    11: OpenOk,
    20: Flow,
    21: FlowOk,
    40: Close,
    41: CloseOk,
}
