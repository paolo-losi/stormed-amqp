
from stormed.util import WithFields

class Declare(WithFields):

    _name      = "exchange.declare"
    _class_id  = 40
    _method_id = 10
    _fields    = [
        (u'ticket'           , u'short'),
        (u'exchange'         , u'shortstr'),
        (u'type'             , u'shortstr'),
        (u'passive'          , u'bit'),
        (u'durable'          , u'bit'),
        (u'auto_delete'      , u'bit'),
        (u'internal'         , u'bit'),
        (u'nowait'           , u'bit'),
        (u'arguments'        , u'table'),
    ]

class DeclareOk(WithFields):

    _name      = "exchange.declare-ok"
    _class_id  = 40
    _method_id = 11
    _fields    = [
    ]

class Delete(WithFields):

    _name      = "exchange.delete"
    _class_id  = 40
    _method_id = 20
    _fields    = [
        (u'ticket'           , u'short'),
        (u'exchange'         , u'shortstr'),
        (u'if_unused'        , u'bit'),
        (u'nowait'           , u'bit'),
    ]

class DeleteOk(WithFields):

    _name      = "exchange.delete-ok"
    _class_id  = 40
    _method_id = 21
    _fields    = [
    ]

class Bind(WithFields):

    _name      = "exchange.bind"
    _class_id  = 40
    _method_id = 30
    _fields    = [
        (u'ticket'           , u'short'),
        (u'destination'      , u'shortstr'),
        (u'source'           , u'shortstr'),
        (u'routing_key'      , u'shortstr'),
        (u'nowait'           , u'bit'),
        (u'arguments'        , u'table'),
    ]

class BindOk(WithFields):

    _name      = "exchange.bind-ok"
    _class_id  = 40
    _method_id = 31
    _fields    = [
    ]

class Unbind(WithFields):

    _name      = "exchange.unbind"
    _class_id  = 40
    _method_id = 40
    _fields    = [
        (u'ticket'           , u'short'),
        (u'destination'      , u'shortstr'),
        (u'source'           , u'shortstr'),
        (u'routing_key'      , u'shortstr'),
        (u'nowait'           , u'bit'),
        (u'arguments'        , u'table'),
    ]

class UnbindOk(WithFields):

    _name      = "exchange.unbind-ok"
    _class_id  = 40
    _method_id = 51
    _fields    = [
    ]


id2method = {
    10: Declare,
    11: DeclareOk,
    20: Delete,
    21: DeleteOk,
    30: Bind,
    31: BindOk,
    40: Unbind,
    51: UnbindOk,
}
