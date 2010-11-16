
from stormed.util import WithFields

class Request(WithFields):

    _name      = "access.request"
    _class_id  = 30
    _method_id = 10
    _fields    = [
        (u'realm'            , u'shortstr'),
        (u'exclusive'        , u'bit'),
        (u'passive'          , u'bit'),
        (u'active'           , u'bit'),
        (u'write'            , u'bit'),
        (u'read'             , u'bit'),
    ]

class RequestOk(WithFields):

    _name      = "access.request-ok"
    _class_id  = 30
    _method_id = 11
    _fields    = [
        (u'ticket'           , u'short'),
    ]


id2method = {
    10: Request,
    11: RequestOk,
}
