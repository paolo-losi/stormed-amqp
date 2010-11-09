import unittest
from stormed.serialization import parse_method, dump_method
from stormed.method.connection import StartOk

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
        self.assertEquals(m.method_id, 10)
        self.assertEquals(m.class_id,  10)
        self.assertEquals(m.version_major, 0)
        self.assertEquals(m.version_minor, 9)
        self.assertEquals(m.server_properties['version'], '2.1.1')
        self.assertEquals(m.mechanisms, 'PLAIN AMQPLAIN')
        self.assertEquals(m.locales, 'en_US')

    def test_dump_startok(self):
        start_ok = StartOk(peer_properties=dict(client="stormed-amqp"),
                           mechanism='PLAIN', response='', locale='en_US')
        data = dump_method(start_ok)
        self.assertEquals(len(data), 48)
        start_ok2 = parse_method(data)
        self.assertEquals(start_ok.mechanism, start_ok2.mechanism)
        self.assertEquals(start_ok.response,  start_ok2.response)
        self.assertEquals(start_ok.locale,    start_ok2.locale)
        self.assertEquals(start_ok.peer_properties['client'],
                          start_ok2.peer_properties['client'])
        

if __name__ == '__main__':
    unittest.main()
