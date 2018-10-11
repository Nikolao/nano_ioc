#
import logging
import unittest
from nano_ioc import Container


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


class IocTestCase(unittest.TestCase):

    def setUp(self):
        self.config = {
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
                'init_function': 'test_nano_ioc.MyClass5.getInstance',
            },
            'service6': {
                'init_function': 'test_nano_ioc.MyClass6.getInstance',
                'init_parameters': ['yep'],
            },
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

    def test_getService_with_dependancy(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service4')
        self.assertTrue(isinstance(tmp, MyClass4))
        tmp = tmp.getService()
        self.assertTrue(isinstance(tmp, MyClass3))

    def test_getService_with_init_function(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service5')
        self.assertTrue(isinstance(tmp, MyClass5))

    def test_getService_with_init_function_and_init_parameters(self):
        obj = Container(self.config, True)
        tmp = obj.getService('service6')
        self.assertTrue(isinstance(tmp, MyClass6))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
#
