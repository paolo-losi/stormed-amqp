import struct

class Start(object):

    method_id = 10
    class_id  = 10
    fields = [
        ('version_major',     'octet'),
        ('version_minor',     'octet'),
        ('server_properties', 'table'),
        ('mechanisms',        'longstr'),
        ('locales',           'longstr'),
    ]


id2method = {
    10: Start,
}
