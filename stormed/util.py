class Enum(object):

    def __init__(self, *names):
        self._names = set(names)

    def __getattr__(self, name):
        if name in self._names:
            return name
        raise AttributeError

class WithFields(object):

    _fields = []

    def __init__(self, **kargs):
        fnames = [ fname for fname, ftype in self._fields ]
        unvalid_kargs = set(kargs.keys()) - set(fnames)
        if unvalid_kargs:
            raise AttributeError('unvalid field name/s: %s' % unvalid_kargs)
        for fn in fnames:
            setattr(self, fn, kargs.get(fn))

def add_method(klass):
    def decorator(f):
        setattr(klass, f.__name__, f)
    return decorator
