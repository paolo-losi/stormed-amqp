
from stormed.util import WithFields

class Select(WithFields):

    _name      = "tx.select"
    _class_id  = 90
    _method_id = 10
    _fields    = [
    ]

class SelectOk(WithFields):

    _name      = "tx.select-ok"
    _class_id  = 90
    _method_id = 11
    _fields    = [
    ]

class Commit(WithFields):

    _name      = "tx.commit"
    _class_id  = 90
    _method_id = 20
    _fields    = [
    ]

class CommitOk(WithFields):

    _name      = "tx.commit-ok"
    _class_id  = 90
    _method_id = 21
    _fields    = [
    ]

class Rollback(WithFields):

    _name      = "tx.rollback"
    _class_id  = 90
    _method_id = 30
    _fields    = [
    ]

class RollbackOk(WithFields):

    _name      = "tx.rollback-ok"
    _class_id  = 90
    _method_id = 31
    _fields    = [
    ]


id2method = {
    10: Select,
    11: SelectOk,
    20: Commit,
    21: CommitOk,
    30: Rollback,
    31: RollbackOk,
}
