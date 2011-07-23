import unittest
from datetime import datetime

from stormed.util import WithFields
from stormed.serialization import parse_method, dump_method, dump, \
                                  parse_timestamp, dump_timestamp
from stormed.method import connection

connection_start_payload = \
    ('\x00\n\x00\n\x00\t\x00\x00\x00\xfb\x07productS\x00\x00\x00\x08RabbitMQ'
     '\x07versionS\x00\x00\x00\x052.1.1\x08platformS\x00\x00\x00\nErlang/OTP'
     '\tcopyrightS\x00\x00\x00gCopyright (C) 2007-2010 LShift Ltd., Cohesive '
     'Financial Technologies LLC., and Rabbit Technologies Ltd.\x0binformation'
     'S\x00\x00\x005Licensed under the MPL.  See http://www.rabbitmq.com/'
     '\x00\x00\x00\x0ePLAIN AMQPLAIN\x00\x00\x00\x05en_US')

class TestMethodSerialization(unittest.TestCase):

    def test_parse_start(self):
        m = parse_method(connection_start_payload)
        self.assertEquals(m._method_id, 10)
        self.assertEquals(m._class_id,  10)
        self.assertEquals(m.version_major, 0)
        self.assertEquals(m.version_minor, 9)
        self.assertEquals(m.server_properties['version'], '2.1.1')
        self.assertEquals(m.mechanisms, 'PLAIN AMQPLAIN')
        self.assertEquals(m.locales, 'en_US')

    def test_parse_dump_startok(self):
        peer_properties = dict(client="stormed-amqp")
        start_ok = connection.StartOk(client_properties=peer_properties,
                                      mechanism='PLAIN', response='',
                                      locale='en_US')
        data = dump_method(start_ok)
        self.assertEquals(len(data), 48)
        start_ok2 = parse_method(data)
        self.assertEquals(start_ok.mechanism, start_ok2.mechanism)
        self.assertEquals(start_ok.response,  start_ok2.response)
        self.assertEquals(start_ok.locale,    start_ok2.locale)
        self.assertEquals(start_ok.client_properties['client'],
                          start_ok2.client_properties['client'])


class TestBitSerialization(unittest.TestCase):

    def test_dump_bit(self):
        class Bunch(WithFields):
            _fields = [('o1', 'octet'),
                       ('b1', 'bit'),
                       ('b2', 'bit'),
                       ('o2', 'octet')]
        o = Bunch(o1=97, b1 = False, b2 = True, o2=98)
        self.assertEquals(dump(o), 'a\x02b')

    def test_dump_bit_at_end(self):
        class Bunch(WithFields):
            _fields = [('o1', 'octet'),
                       ('b1', 'bit'),
                       ('b2', 'bit'),
                       ('b3', 'bit')]
        o = Bunch(o1=97, b1 = False, b2 = True, b3=True)
        self.assertEquals(dump(o), 'a\x06')

class TestTimeStamp(unittest.TestCase):

    def test_from_to(self):
        dt = datetime(2011, 1, 1, 10, 5)
        dt2, offset = parse_timestamp(dump_timestamp(dt), 0)
        self.assertEquals(dt, dt2)

    def test_from(self):
        parsed_dt, offset = parse_timestamp('\x00\x00\x00\x00M\x1e`p', 0)
        self.assertEquals(offset, 8)
        self.assertEquals(parsed_dt, datetime(2011, 1, 1))

    def test_to(self):
        dt = datetime(2011, 1, 1)
        self.assertEquals(dump_timestamp(dt), '\x00\x00\x00\x00M\x1e`p')


if __name__ == '__main__':
    unittest.main()
