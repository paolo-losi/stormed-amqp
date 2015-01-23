import logging

logger = logging.getLogger('stormed-amqp')

class AmqpError(Exception): pass

class AmqpStatusError(AmqpError): pass

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
            raise AttributeError('invalid field name/s: %s' % unvalid_kargs)
        for fn in fnames:
            setattr(self, fn, kargs.get(fn))

    def __repr__(self):
        fs = ['%s=%r' % (f, getattr(self,f)) for f, _ in self._fields]
        t = type(self)
        klass = (getattr(self, '_name', None) or
                 '%s.%s' % (t.__module__, t.__name__))
        return '%s(%s)' % (klass, ', '.join(fs))

def add_method(klass):
    def decorator(f):
        setattr(klass, f.__name__, f)
    return decorator
