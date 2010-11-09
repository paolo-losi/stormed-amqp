import struct
from stormed.util import WithFields

class Start(WithFields):

    name = 'connection.start'
    class_id  = 10
    method_id = 10
    fields = [
        ('version_major',     'octet'),
        ('version_minor',     'octet'),
        ('server_properties', 'table'),
        ('mechanisms',        'longstr'),
        ('locales',           'longstr'),
    ]

class StartOk(WithFields):

    name = 'connection.start-ok'
    class_id  = 10
    method_id = 11
    fields = [
        ('peer_properties',   'table'),
        ('mechanism',         'shortstr'),
        ('response',          'longstr'),
        ('locale',            'shortstr'),
    ]

class Tune(WithFields):

    name = 'connection.tune'
    class_id  = 10
    method_id = 30
    fields = [
        ('channel_max',       'short'),
        ('frame_max',         'long'),
        ('hearbeat',          'short'),
    ]

class TuneOk(WithFields):

    name = 'connection.tune-ok'
    class_id  = 10
    method_id = 31
    fields = [
        ('channel_max',       'short'),
        ('frame_max',         'long'),
        ('hearbeat',          'short'),
    ]

class Open(WithFields):

    name = 'connection.open'
    class_id = 10
    method_id = 40
    fields = [
        ('virtual_host',      'shortstr'),
        ('capabilities',      'shortstr'), #deprecated
        ('insist',            'octet'), #deprecated
    ]

class OpenOk(WithFields):

    name = 'connection.open-ok'
    class_id = 10
    method_id = 41
    fields = [
        ('known_hosts',      'shortstr'), #deprecated
    ]

class Close(WithFields):

    name = 'connection.close'
    class_id = 10
    method_id = 50
    fields = [
        ('reply_code',       'short'),
        ('reply_text',       'shortstr'),
        ('_class_id',         'short'),
        ('_method_id',        'short'),
    ]

class CloseOk(WithFields):

    name = 'connection.close-ok'
    class_id = 10
    method_id = 51
    fields = [
    ]


id2method = {
    10: Start,
    11: StartOk,
    30: Tune,
    31: TuneOk,
    40: Open,
    41: OpenOk,
    50: Close,
    51: CloseOk,
}
