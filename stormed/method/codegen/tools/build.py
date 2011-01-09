#! /usr/bin/env python

import json
import os.path
from keyword import iskeyword

codegen_dir = os.path.join(os.path.dirname(__file__), '..')

json_source = os.path.join(os.path.dirname(__file__),
                           'amqp-rabbitmq-0.9.1.json')

def gen_constant(specs):
    constants_filename = os.path.join(codegen_dir, '..', 'constant.py')
    fout = open(constants_filename, 'w')
    for c in specs['constants']:
        c['name'] = fix_name(c['name'])
        template = '%(name)-20s = %(value)r %(comment)s\n'
        c.update(comment = '# %(class)s' % c if 'class' in c else '')
        fout.write(template % c)
    fout.write('\nid2constant = {\n')
    for c in specs['constants']:
        c['name'] = fix_name(c['name'])
        template = '    %(value)4r: "%(name)s",\n'
        fout.write(template % c)
    fout.write('}\n')
        

properties_template = "properties = [\n%s\n]\n\n"

def gen_properties(properties):
    if not properties:
        return ""
    prop_s = [ "        (%-20r, %r),\n" % (fix_name(p['name']),
                                           str(p['type']))
               for p in properties ]
    return properties_template % (''.join(prop_s))
        

file_template = \
"""
from stormed.util import WithFields

%s%s

id2method = {
%s
}
"""

method_template = \
"""class %(klass_name)s(WithFields):

    _name      = "%(class_name)s.%(method_name)s"
    _class_id  = %(class_id)d
    _method_id = %(method_id)d
    _sync      = %(sync)s
    _content   = %(content)s
    _fields    = [%(fields)s
    ]
"""

def gen_methods(specs):
    domains = dict( (k,v) for k,v in specs['domains'] )
    for c in specs['classes']:
        class_filename = os.path.join(codegen_dir, '%s.py' % c['name'])
        method_classes = []
        id2method_entries = []
        for m in c['methods']:
            fields = []
            for f in m['arguments']:
                typ = f['type'] if 'type' in f else domains[f['domain']]
                fname = fix_name(f['name'])
                fields.append("\n        (%-20r, %r)," % (fname, str(typ)))
            klass_name = _camel_case(m['name'])
            method_classes.append(method_template % dict(
                klass_name  = klass_name,
                class_name  = c['name'],
                method_name = m['name'],
                class_id    = c['id'],
                method_id   = m['id'],
                sync        = m.get('synchronous', False),
                content     = m.get('content', False),
                fields      = ''.join(fields),
            ))
            id2method_entries.append('    %-2d: %s,' % (m['id'], klass_name))

        properties = gen_properties(c.get('properties', []))
        s = file_template % (properties,
                             '\n'.join(method_classes),
                             '\n'.join(id2method_entries))
        fout = open(class_filename, 'w')
        fout.write(s)
        fout.close()

init_template = \
"""%s

id2class = {
%s
}
"""

def gen_classes(specs):
    init_filename = os.path.join(codegen_dir, '__init__.py')
    imports = []
    id2class_entries = []
    for c in specs['classes']:
        imports.append('from stormed.method.codegen import %s' % c['name'])
        id2class_entries.append('    %-2d: %s,' % (c['id'], c['name']))
    
    s = init_template % ('\n'.join(imports),
                         '\n'.join(id2class_entries))
    fout = open(init_filename, 'w')
    fout.write(s)
    fout.close()

def main():
    specs = json.load(open(json_source))
    gen_constant(specs)
    gen_methods(specs)
    gen_classes(specs)

def _camel_case(s):
    return s.title().replace('-', '')

def fix_name(s):
    s = s.replace(' ','_').replace('-','_').encode('ascii')
    return "_"+s if iskeyword(s) else s
        

if __name__ == '__main__':
    main()
