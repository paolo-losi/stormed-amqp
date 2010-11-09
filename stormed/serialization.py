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

def dump(fields, o):
    dumped_vals = []
    for name, typ in o.fields:
        dumper = globals()['dump_%s' % typ]
        v = dumper(getattr(o, name))
        dumped_vals.append(v)
    return ''.join(dumped_vals)

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

def dump_method(m):
    header = method_header.pack(m.class_id, m.method_id)
    dumped_vals = dump(m.fields, m)
    return '%s%s' % (header, dumped_vals)
    

# --- low level parsing ---
    
def parse_octet(data, offset):
    return ord(data[offset]), offset+1

def dump_octet(i):
    return chr(i)

short = Struct('!H')
def parse_short(data, offset):
    val = short.unpack_from(data, offset)[0]
    return val, offset+2

def dump_short(i):
    return short.pack(i)

_long = Struct('!L')
def parse_long(data, offset):
    val = _long.unpack_from(data, offset)[0]
    return val, offset+4

def dump_long(i):
    return _long.pack(i)

longstr_header = Struct('!L')
def parse_longstr(data, offset):
    l = longstr_header.unpack_from(data, offset)[0]
    val = data[offset+4: offset+4+l]
    return val, offset+4+l

def dump_longstr(s):
    encoded_s = s.encode('utf8')
    return '%s%s' % (longstr_header.pack(len(encoded_s)), encoded_s)

def parse_shortstr(data, offset):
    l = ord(data[offset])
    val = data[offset+1: offset+1+l]
    return val, offset+1+l

def dump_shortstr(s):
    encoded_s = s.encode('utf8')
    return '%s%s' % (chr(len(encoded_s)), encoded_s)
    

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

def table2str(d):
    return ''.join([ '%sS%s' % (dump_shortstr(k), dump_longstr(v))
                     for k, v in d.items() ])
def dump_table(d):
    entries = table2str(d)    
    return dump_longstr(entries)
