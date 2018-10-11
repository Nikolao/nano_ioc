#
import importlib
import logging


class Container:
    def __init__(self, configuration, debug=False):
        logging.debug('IN Container __init')
        self._debug = debug
        self._configuration = configuration
        self._services = {}

        for service_name in self._configuration:
            create = self._configuration[service_name].get(
                'create-at-init', False)
            if create:
                self._initService(service_name)
        logging.debug('OUT Container __init')

    def getService(self, service_name):
        if (service_name not in self._services):
            self._initService(service_name)
        return self._services[service_name]

    def _initService(self, service_name):
        logging.debug('IN _initService {}'.format(service_name))
        if service_name in self._services:
            logging.debug("Error {} already initialized".format(service_name))
            logging.debug('OUT _initService {}'.format(service_name))
            return

        with_constructor = self._configuration[service_name].get('class', None)
        with_function = self._configuration[service_name].get(
            'init_function', None)
        with_parameters = self._configuration[service_name].get(
            'init_parameters', None)

        param = []
        if with_parameters:
            for par in with_parameters:
                if isinstance(par, str):
                    if par[0] == '@':
                        par = self._initService(par[1:])
                param.append(par)

        instance = None

        if with_constructor:
            module_name, class_name = with_constructor.rsplit('.', 1)
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            instance = class_(*param)
        elif with_function:
            module_name, class_name, method_name = with_function.rsplit('.', 2)
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            method = getattr(class_, method_name)
            instance = method(class_, *param)
        else:
            logging.debug("Error no class for {}".format(service_name))
            logging.debug('OUT _initService {}'.format(service_name))
            return

        self._services[service_name] = instance

        logging.debug('_initService {} '.format(instance))
        logging.debug('OUT _initService {} OK'.format(service_name))
        return self._services[service_name]

#
