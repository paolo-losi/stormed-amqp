
from stormed.util import WithFields

class Declare(WithFields):

    _name      = "queue.declare"
    _class_id  = 50
    _method_id = 10
    _sync      = True
    _content   = False
    _fields    = [
        ('ticket'            , 'short'),
        ('queue'             , 'shortstr'),
        ('passive'           , 'bit'),
        ('durable'           , 'bit'),
        ('exclusive'         , 'bit'),
        ('auto_delete'       , 'bit'),
        ('nowait'            , 'bit'),
        ('arguments'         , 'table'),
    ]

class DeclareOk(WithFields):

    _name      = "queue.declare-ok"
    _class_id  = 50
    _method_id = 11
    _sync      = False
    _content   = False
    _fields    = [
        ('queue'             , 'shortstr'),
        ('message_count'     , 'long'),
        ('consumer_count'    , 'long'),
    ]

class Bind(WithFields):

    _name      = "queue.bind"
    _class_id  = 50
    _method_id = 20
    _sync      = True
    _content   = False
    _fields    = [
        ('ticket'            , 'short'),
        ('queue'             , 'shortstr'),
        ('exchange'          , 'shortstr'),
        ('routing_key'       , 'shortstr'),
        ('nowait'            , 'bit'),
        ('arguments'         , 'table'),
    ]

class BindOk(WithFields):

    _name      = "queue.bind-ok"
    _class_id  = 50
    _method_id = 21
    _sync      = False
    _content   = False
    _fields    = [
    ]

class Purge(WithFields):

    _name      = "queue.purge"
    _class_id  = 50
    _method_id = 30
    _sync      = True
    _content   = False
    _fields    = [
        ('ticket'            , 'short'),
        ('queue'             , 'shortstr'),
        ('nowait'            , 'bit'),
    ]

class PurgeOk(WithFields):

    _name      = "queue.purge-ok"
    _class_id  = 50
    _method_id = 31
    _sync      = False
    _content   = False
    _fields    = [
        ('message_count'     , 'long'),
    ]

class Delete(WithFields):

    _name      = "queue.delete"
    _class_id  = 50
    _method_id = 40
    _sync      = True
    _content   = False
    _fields    = [
        ('ticket'            , 'short'),
        ('queue'             , 'shortstr'),
        ('if_unused'         , 'bit'),
        ('if_empty'          , 'bit'),
        ('nowait'            , 'bit'),
    ]

class DeleteOk(WithFields):

    _name      = "queue.delete-ok"
    _class_id  = 50
    _method_id = 41
    _sync      = False
    _content   = False
    _fields    = [
        ('message_count'     , 'long'),
    ]

class Unbind(WithFields):

    _name      = "queue.unbind"
    _class_id  = 50
    _method_id = 50
    _sync      = True
    _content   = False
    _fields    = [
        ('ticket'            , 'short'),
        ('queue'             , 'shortstr'),
        ('exchange'          , 'shortstr'),
        ('routing_key'       , 'shortstr'),
        ('arguments'         , 'table'),
    ]

class UnbindOk(WithFields):

    _name      = "queue.unbind-ok"
    _class_id  = 50
    _method_id = 51
    _sync      = False
    _content   = False
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
