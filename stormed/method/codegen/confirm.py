
from stormed.util import WithFields

class Select(WithFields):

    _name      = "confirm.select"
    _class_id  = 85
    _method_id = 10
    _sync      = True
    _content   = False
    _fields    = [
        ('nowait'            , 'bit'),
    ]

class SelectOk(WithFields):

    _name      = "confirm.select-ok"
    _class_id  = 85
    _method_id = 11
    _sync      = False
    _content   = False
    _fields    = [
    ]


id2method = {
    10: Select,
    11: SelectOk,
}
