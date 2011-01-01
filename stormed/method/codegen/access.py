
from stormed.util import WithFields

class Request(WithFields):

    _name      = "access.request"
    _class_id  = 30
    _method_id = 10
    _sync      = True
    _content   = False
    _fields    = [
        ('realm'             , 'shortstr'),
        ('exclusive'         , 'bit'),
        ('passive'           , 'bit'),
        ('active'            , 'bit'),
        ('write'             , 'bit'),
        ('read'              , 'bit'),
    ]

class RequestOk(WithFields):

    _name      = "access.request-ok"
    _class_id  = 30
    _method_id = 11
    _sync      = False
    _content   = False
    _fields    = [
        ('ticket'            , 'short'),
    ]


id2method = {
    10: Request,
    11: RequestOk,
}
