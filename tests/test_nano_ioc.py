#
import os
import logging
import unittest
from nano_ioc import Container


global count
count = 0


def getMyClass0(num, status):
    logging.debug('function getMyClass0 {} {}'.format(num, status))
    return MyClass0()


class MyClass0:
    def __init__(self):
        global count
        count = count + 1
        self.count = count
        print('class MyClass0 __init {}'.format(self.count))
        logging.debug('class MyClass0 __init {}'.format(self.count))


class MyClass1:
    def __init__(self):
        logging.debug('class MyClass1 __init')


class MyClass2:
    def __init__(self):
        logging.debug('class MyClass2 __init')


class MyClass2_5:
    def __init__(self, num, st):
        self.info = "{} {}".format(num, st)
        logging.debug(
            'class MyClass3 __init : {} {} {}'.format(num, st, self.info))


class MyClass3:
    def __init__(self, num, st):
        self.info = "{} {}".format(num, st)
        logging.debug(
            'class MyClass3 __init : {} {} {}'.format(num, st, self.info))


class MyClass4:
    def __init__(self, service3):
        self.service3 = service3
        logging.debug('class MyClass4 __init : "{}"'.format(service3.info))

    def getService(self):
        return self.service3


class MyClass5:
    def __init__(self):
        logging.debug('class MyClass5 __init')

    @staticmethod
    def getInstance(class_):
        logging.debug('class MyClass5 getInstance')
        return MyClass5()


class MyClass6:
    def __init__(self):
        logging.debug('class MyClass6 __init')

    @staticmethod
    def getInstance(class_, arg):
        logging.debug('class MyClass6 getInstance {}'.format(arg))
        return MyClass6()


class MyClass7:
    def __init__(self):
        logging.debug('class MyClass7 __init')

    def setSize(self, arg):
        self.size = arg

    def setLogger(self, arg):
        self.logger = arg


class MyClass8:
    def __init__(self, arg):
        self.user = arg
        logging.debug('class MyClass7 __init')


class IocTestCase(unittest.TestCase):

    def setUp(self):
        self.config = {
            'service_prefix': '@',
            'variable_prefix': '$',
            'services': {
                'service0': {
                    'init_function': 'test_nano_ioc.getMyClass0',
                    'init_parameters': [0, 'ok'],
                },
                'multi': {
                    'singleton': False,
                    'class': 'test_nano_ioc.MyClass0',
                },
                'service1': {
                    'create-at-init': True,
                    'class': 'test_nano_ioc.MyClass1',
                },
                'service2': {
                    'create-at-init': False,
                    'class': 'test_nano_ioc.MyClass2',
                },
                'service2_5': {
                    'class': 'test_nano_ioc.MyClass2_5',
                    'init_parameters': [1, 'ok'],
                },
                'service3': {
                    'class': 'test_nano_ioc.MyClass3',
                    'init_parameters': [1, 'ok'],
                },
                'service4': {
                    'class': 'test_nano_ioc.MyClass4',
                    'init_parameters': ['@service3'],
                },
                'service5': {
                    'init_method': 'test_nano_ioc.MyClass5.getInstance',
                },
                'service6': {
                    'init_method': 'test_nano_ioc.MyClass6.getInstance',
                    'init_parameters': ['yep'],
                },
                'service7': {
                    'class': 'test_nano_ioc.MyClass7',
                    'post_creation': [
                        {
                            'method': 'test_nano_ioc.MyClass7.setSize',
                            'parameters': [42]
                        },
                        {
                            'method': 'test_nano_ioc.MyClass7.setLogger',
                            'parameters': ['@service4']
                        },
                    ]
                },
                'service8': {
                    'class': 'test_nano_ioc.MyClass8',
                    'init_parameters': ['$USER'],
                },
            }
        }

    def test_getService_with_create_at_init(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service1')
        self.assertTrue(isinstance(tmp, MyClass1))

    def test_getService_without_create_at_init(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service2')
        self.assertTrue(isinstance(tmp, MyClass2))

    def test_getService_with_init_parameters(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service2_5')
        self.assertTrue(isinstance(tmp, MyClass2_5))

    def test_getService_with_service_dependancy(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service4')
        self.assertTrue(isinstance(tmp, MyClass4))
        tmp = tmp.getService()
        self.assertTrue(isinstance(tmp, MyClass3))

    def test_getService_with_init_function(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service0')
        self.assertTrue(isinstance(tmp, MyClass0))

    def test_getService_with_init_method(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service5')
        self.assertTrue(isinstance(tmp, MyClass5))

    def test_getService_with_init_function_and_init_parameters(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service6')
        self.assertTrue(isinstance(tmp, MyClass6))

    def test_getService_multiple(self):
        obj = Container(self.config, True)
        tmp1 = obj.getService('multi')
        self.assertTrue(isinstance(tmp1, MyClass0))
        tmp2 = obj.getService('multi')
        self.assertTrue(isinstance(tmp2, MyClass0))
        self.assertNotEquals(tmp1.count, tmp2.count)

    def test_getService_singleton(self):
        obj = Container(self.config, True)
        tmp1 = obj.getService('service0')
        self.assertTrue(isinstance(tmp1, MyClass0))
        tmp2 = obj.getService('service0')
        self.assertTrue(isinstance(tmp2, MyClass0))
        self.assertEquals(tmp1.count, tmp2.count)

    def test_getService_with_post_create_method(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service7')
        self.assertTrue(isinstance(tmp, MyClass7))
        self.assertNotEquals(None, tmp.logger)
        self.assertEquals(42, tmp.size)

    def test_getService_with_env_variable_dependancy(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service8')
        self.assertTrue(isinstance(tmp, MyClass8))
        self.assertEquals(os.environ['USER'], tmp.user)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
#
