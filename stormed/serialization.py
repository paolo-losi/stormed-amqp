from struct import Struct
from itertools import izip

from stormed import method

def parse(fields, data):
    vals = []
    offset = 0
    for f in fields:
        parser = globals()['parse_%s' % f]
        val, offset = parser(data, offset)
        vals.append(val)
    assert offset == len(data)
    return vals

method_header = Struct('!HH')
def parse_method(data):
    class_id, method_id = method_header.unpack(data[:4])
    mod = method.id2class[class_id]
    inst = getattr(mod, 'id2method')[method_id]()
    names = [ name for name, typ in inst.fields ]
    types = [ typ  for name, typ in inst.fields ]
    vals = parse(types, data[4:])
    for name, val in izip(names, vals):
        setattr(inst, name, val)
    return inst

# --- low level parsing ---
    
def parse_octet(data, offset):
    return ord(data[offset]), offset+1

short = Struct('!H')
def parse_short(data, offset):
    val = short.unpack_from(data, offset)[0]
    return val, offset+2

longstr_header = Struct('!L')
def parse_longstr(data, offset):
    l = longstr_header.unpack_from(data, offset)[0]
    val = data[offset+4: offset+4+l]
    return val, offset+4+l

def parse_shortstr(data, offset):
    l = ord(data[offset])
    val = data[offset+1: offset+1+l]
    return val, offset+1+l

field_type_dict = {
  's': parse_shortstr,
  'S': parse_longstr,
}

def parse_table(data, offset):
    s, new_offset = parse_longstr(data, offset)
    d = {}
    s_len = len(s)
    offset = 0
    while offset < s_len:
        key, offset = parse_shortstr(s, offset)
        typ = s[offset]
        assert typ in field_type_dict, typ
        val, offset = field_type_dict[typ](s, offset+1)
        d[key] = val
    return d, new_offset
