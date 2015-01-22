
from stormed.util import WithFields

properties = [
        ('content_type'      , 'shortstr'),
        ('content_encoding'  , 'shortstr'),
        ('headers'           , 'table'),
        ('delivery_mode'     , 'octet'),
        ('priority'          , 'octet'),
        ('correlation_id'    , 'shortstr'),
        ('reply_to'          , 'shortstr'),
        ('expiration'        , 'shortstr'),
        ('message_id'        , 'shortstr'),
        ('timestamp'         , 'timestamp'),
        ('type'              , 'shortstr'),
        ('user_id'           , 'shortstr'),
        ('app_id'            , 'shortstr'),
        ('cluster_id'        , 'shortstr'),

]

class Qos(WithFields):

    _name      = "basic.qos"
    _class_id  = 60
    _method_id = 10
    _sync      = True
    _content   = False
    _fields    = [
        ('prefetch_size'     , 'long'),
        ('prefetch_count'    , 'short'),
        ('_global'           , 'bit'),
    ]

class QosOk(WithFields):

    _name      = "basic.qos-ok"
    _class_id  = 60
    _method_id = 11
    _sync      = False
    _content   = False
    _fields    = [
    ]

class Consume(WithFields):

    _name      = "basic.consume"
    _class_id  = 60
    _method_id = 20
    _sync      = True
    _content   = False
    _fields    = [
        ('ticket'            , 'short'),
        ('queue'             , 'shortstr'),
        ('consumer_tag'      , 'shortstr'),
        ('no_local'          , 'bit'),
        ('no_ack'            , 'bit'),
        ('exclusive'         , 'bit'),
        ('nowait'            , 'bit'),
        ('arguments'         , 'table'),
    ]

class ConsumeOk(WithFields):

    _name      = "basic.consume-ok"
    _class_id  = 60
    _method_id = 21
    _sync      = False
    _content   = False
    _fields    = [
        ('consumer_tag'      , 'shortstr'),
    ]

class Cancel(WithFields):

    _name      = "basic.cancel"
    _class_id  = 60
    _method_id = 30
    _sync      = True
    _content   = False
    _fields    = [
        ('consumer_tag'      , 'shortstr'),
        ('nowait'            , 'bit'),
    ]

class CancelOk(WithFields):

    _name      = "basic.cancel-ok"
    _class_id  = 60
    _method_id = 31
    _sync      = False
    _content   = False
    _fields    = [
        ('consumer_tag'      , 'shortstr'),
    ]

class Publish(WithFields):

    _name      = "basic.publish"
    _class_id  = 60
    _method_id = 40
    _sync      = False
    _content   = True
    _fields    = [
        ('ticket'            , 'short'),
        ('exchange'          , 'shortstr'),
        ('routing_key'       , 'shortstr'),
        ('mandatory'         , 'bit'),
        ('immediate'         , 'bit'),
    ]

class Return(WithFields):

    _name      = "basic.return"
    _class_id  = 60
    _method_id = 50
    _sync      = False
    _content   = True
    _fields    = [
        ('reply_code'        , 'short'),
        ('reply_text'        , 'shortstr'),
        ('exchange'          , 'shortstr'),
        ('routing_key'       , 'shortstr'),
    ]

class Deliver(WithFields):

    _name      = "basic.deliver"
    _class_id  = 60
    _method_id = 60
    _sync      = False
    _content   = True
    _fields    = [
        ('consumer_tag'      , 'shortstr'),
        ('delivery_tag'      , 'longlong'),
        ('redelivered'       , 'bit'),
        ('exchange'          , 'shortstr'),
        ('routing_key'       , 'shortstr'),
    ]

class Get(WithFields):

    _name      = "basic.get"
    _class_id  = 60
    _method_id = 70
    _sync      = True
    _content   = False
    _fields    = [
        ('ticket'            , 'short'),
        ('queue'             , 'shortstr'),
        ('no_ack'            , 'bit'),
    ]

class GetOk(WithFields):

    _name      = "basic.get-ok"
    _class_id  = 60
    _method_id = 71
    _sync      = False
    _content   = True
    _fields    = [
        ('delivery_tag'      , 'longlong'),
        ('redelivered'       , 'bit'),
        ('exchange'          , 'shortstr'),
        ('routing_key'       , 'shortstr'),
        ('message_count'     , 'long'),
    ]

class GetEmpty(WithFields):

    _name      = "basic.get-empty"
    _class_id  = 60
    _method_id = 72
    _sync      = False
    _content   = False
    _fields    = [
        ('cluster_id'        , 'shortstr'),
    ]

class Ack(WithFields):

    _name      = "basic.ack"
    _class_id  = 60
    _method_id = 80
    _sync      = False
    _content   = False
    _fields    = [
        ('delivery_tag'      , 'longlong'),
        ('multiple'          , 'bit'),
    ]

class Reject(WithFields):

    _name      = "basic.reject"
    _class_id  = 60
    _method_id = 90
    _sync      = False
    _content   = False
    _fields    = [
        ('delivery_tag'      , 'longlong'),
        ('requeue'           , 'bit'),
    ]

class RecoverAsync(WithFields):

    _name      = "basic.recover-async"
    _class_id  = 60
    _method_id = 100
    _sync      = False
    _content   = False
    _fields    = [
        ('requeue'           , 'bit'),
    ]

class Recover(WithFields):

    _name      = "basic.recover"
    _class_id  = 60
    _method_id = 110
    _sync      = True
    _content   = False
    _fields    = [
        ('requeue'           , 'bit'),
    ]

class RecoverOk(WithFields):

    _name      = "basic.recover-ok"
    _class_id  = 60
    _method_id = 111
    _sync      = False
    _content   = False
    _fields    = [
    ]

class Nack(WithFields):

    _name      = "basic.nack"
    _class_id  = 60
    _method_id = 120
    _sync      = False
    _content   = False
    _fields    = [
        ('delivery_tag'      , 'longlong'),
        ('multiple'          , 'bit'),
        ('requeue'           , 'bit'),
    ]


id2method = {
    10: Qos,
    11: QosOk,
    20: Consume,
    21: ConsumeOk,
    30: Cancel,
    31: CancelOk,
    40: Publish,
    50: Return,
    60: Deliver,
    70: Get,
    71: GetOk,
    72: GetEmpty,
    80: Ack,
    90: Reject,
    100: RecoverAsync,
    110: Recover,
    111: RecoverOk,
    120: Nack,
}
