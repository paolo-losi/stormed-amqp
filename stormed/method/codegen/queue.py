
from stormed.util import WithFields

class Declare(WithFields):

    _name      = "queue.declare"
    _class_id  = 50
    _method_id = 10
    _fields    = [
        (u'ticket'           , u'short'),
        (u'queue'            , u'shortstr'),
        (u'passive'          , u'bit'),
        (u'durable'          , u'bit'),
        (u'exclusive'        , u'bit'),
        (u'auto_delete'      , u'bit'),
        (u'nowait'           , u'bit'),
        (u'arguments'        , u'table'),
    ]

class DeclareOk(WithFields):

    _name      = "queue.declare-ok"
    _class_id  = 50
    _method_id = 11
    _fields    = [
        (u'queue'            , u'shortstr'),
        (u'message_count'    , u'long'),
        (u'consumer_count'   , u'long'),
    ]

class Bind(WithFields):

    _name      = "queue.bind"
    _class_id  = 50
    _method_id = 20
    _fields    = [
        (u'ticket'           , u'short'),
        (u'queue'            , u'shortstr'),
        (u'exchange'         , u'shortstr'),
        (u'routing_key'      , u'shortstr'),
        (u'nowait'           , u'bit'),
        (u'arguments'        , u'table'),
    ]

class BindOk(WithFields):

    _name      = "queue.bind-ok"
    _class_id  = 50
    _method_id = 21
    _fields    = [
    ]

class Purge(WithFields):

    _name      = "queue.purge"
    _class_id  = 50
    _method_id = 30
    _fields    = [
        (u'ticket'           , u'short'),
        (u'queue'            , u'shortstr'),
        (u'nowait'           , u'bit'),
    ]

class PurgeOk(WithFields):

    _name      = "queue.purge-ok"
    _class_id  = 50
    _method_id = 31
    _fields    = [
        (u'message_count'    , u'long'),
    ]

class Delete(WithFields):

    _name      = "queue.delete"
    _class_id  = 50
    _method_id = 40
    _fields    = [
        (u'ticket'           , u'short'),
        (u'queue'            , u'shortstr'),
        (u'if_unused'        , u'bit'),
        (u'if_empty'         , u'bit'),
        (u'nowait'           , u'bit'),
    ]

class DeleteOk(WithFields):

    _name      = "queue.delete-ok"
    _class_id  = 50
    _method_id = 41
    _fields    = [
        (u'message_count'    , u'long'),
    ]

class Unbind(WithFields):

    _name      = "queue.unbind"
    _class_id  = 50
    _method_id = 50
    _fields    = [
        (u'ticket'           , u'short'),
        (u'queue'            , u'shortstr'),
        (u'exchange'         , u'shortstr'),
        (u'routing_key'      , u'shortstr'),
        (u'arguments'        , u'table'),
    ]

class UnbindOk(WithFields):

    _name      = "queue.unbind-ok"
    _class_id  = 50
    _method_id = 51
    _fields    = [
    ]


id2method = {
    10: Declare,
    11: DeclareOk,
    20: Bind,
    21: BindOk,
    30: Purge,
    31: PurgeOk,
    40: Delete,
    41: DeleteOk,
    50: Unbind,
    51: UnbindOk,
}
