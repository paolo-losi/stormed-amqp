
from stormed.util import WithFields

class Qos(WithFields):

    _name      = "basic.qos"
    _class_id  = 60
    _method_id = 10
    _fields    = [
        (u'prefetch_size'    , u'long'),
        (u'prefetch_count'   , u'short'),
        (u'global'           , u'bit'),
    ]

class QosOk(WithFields):

    _name      = "basic.qos-ok"
    _class_id  = 60
    _method_id = 11
    _fields    = [
    ]

class Consume(WithFields):

    _name      = "basic.consume"
    _class_id  = 60
    _method_id = 20
    _fields    = [
        (u'ticket'           , u'short'),
        (u'queue'            , u'shortstr'),
        (u'consumer_tag'     , u'shortstr'),
        (u'no_local'         , u'bit'),
        (u'no_ack'           , u'bit'),
        (u'exclusive'        , u'bit'),
        (u'nowait'           , u'bit'),
        (u'arguments'        , u'table'),
    ]

class ConsumeOk(WithFields):

    _name      = "basic.consume-ok"
    _class_id  = 60
    _method_id = 21
    _fields    = [
        (u'consumer_tag'     , u'shortstr'),
    ]

class Cancel(WithFields):

    _name      = "basic.cancel"
    _class_id  = 60
    _method_id = 30
    _fields    = [
        (u'consumer_tag'     , u'shortstr'),
        (u'nowait'           , u'bit'),
    ]

class CancelOk(WithFields):

    _name      = "basic.cancel-ok"
    _class_id  = 60
    _method_id = 31
    _fields    = [
        (u'consumer_tag'     , u'shortstr'),
    ]

class Publish(WithFields):

    _name      = "basic.publish"
    _class_id  = 60
    _method_id = 40
    _fields    = [
        (u'ticket'           , u'short'),
        (u'exchange'         , u'shortstr'),
        (u'routing_key'      , u'shortstr'),
        (u'mandatory'        , u'bit'),
        (u'immediate'        , u'bit'),
    ]

class Return(WithFields):

    _name      = "basic.return"
    _class_id  = 60
    _method_id = 50
    _fields    = [
        (u'reply_code'       , u'short'),
        (u'reply_text'       , u'shortstr'),
        (u'exchange'         , u'shortstr'),
        (u'routing_key'      , u'shortstr'),
    ]

class Deliver(WithFields):

    _name      = "basic.deliver"
    _class_id  = 60
    _method_id = 60
    _fields    = [
        (u'consumer_tag'     , u'shortstr'),
        (u'delivery_tag'     , u'longlong'),
        (u'redelivered'      , u'bit'),
        (u'exchange'         , u'shortstr'),
        (u'routing_key'      , u'shortstr'),
    ]

class Get(WithFields):

    _name      = "basic.get"
    _class_id  = 60
    _method_id = 70
    _fields    = [
        (u'ticket'           , u'short'),
        (u'queue'            , u'shortstr'),
        (u'no_ack'           , u'bit'),
    ]

class GetOk(WithFields):

    _name      = "basic.get-ok"
    _class_id  = 60
    _method_id = 71
    _fields    = [
        (u'delivery_tag'     , u'longlong'),
        (u'redelivered'      , u'bit'),
        (u'exchange'         , u'shortstr'),
        (u'routing_key'      , u'shortstr'),
        (u'message_count'    , u'long'),
    ]

class GetEmpty(WithFields):

    _name      = "basic.get-empty"
    _class_id  = 60
    _method_id = 72
    _fields    = [
        (u'cluster_id'       , u'shortstr'),
    ]

class Ack(WithFields):

    _name      = "basic.ack"
    _class_id  = 60
    _method_id = 80
    _fields    = [
        (u'delivery_tag'     , u'longlong'),
        (u'multiple'         , u'bit'),
    ]

class Reject(WithFields):

    _name      = "basic.reject"
    _class_id  = 60
    _method_id = 90
    _fields    = [
        (u'delivery_tag'     , u'longlong'),
        (u'requeue'          , u'bit'),
    ]

class RecoverAsync(WithFields):

    _name      = "basic.recover-async"
    _class_id  = 60
    _method_id = 100
    _fields    = [
        (u'requeue'          , u'bit'),
    ]

class Recover(WithFields):

    _name      = "basic.recover"
    _class_id  = 60
    _method_id = 110
    _fields    = [
        (u'requeue'          , u'bit'),
    ]

class RecoverOk(WithFields):

    _name      = "basic.recover-ok"
    _class_id  = 60
    _method_id = 111
    _fields    = [
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
}
