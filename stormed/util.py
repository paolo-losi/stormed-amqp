class Enum(object):

    def __init__(self, *names):
        self._names = set(names)

    def __getattr__(self, name):
        if name in self._names:
            return name
        raise AttributeError

class WithFields(object):

    fields = []
    
    def __init__(self, **kargs):
        fnames = [ fname for fname, ftype in self.fields ]
        for k,v in kargs.items():
            if k in fnames:
                setattr(self, k, v)
            else:
                raise AttributeError('%r in not a valid field name' % k)
