import unittest
from stormed.serialization import parse_method

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

if __name__ == '__main__':
    unittest.main()
