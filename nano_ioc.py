#
import os
import importlib


class Container:
    def __init__(self, configuration, debug=False):
        self._debug = debug
        self._configuration = configuration
        self._services = {}

        for service_name in self._configuration['services']:
            conf = self._configuration['services'][service_name]
            create = conf.get('create-at-init', False)
            if create:
                self._initService(service_name)

    def getService(self, service_name):
        ret = None
        if (service_name not in self._services):
            ret = self._initService(service_name)
        else:
            ret = self._services[service_name]
        return ret

    def _initService(self, service_name):
        if service_name in self._services:
            raise Exception("{} already initialized".format(service_name))

        service_prefix = self._configuration.get('service_prefix', '@')
        variable_prefix = self._configuration.get('variable_prefix', '$')

        conf = self._configuration['services'][service_name]
        singleton = conf.get('singleton', True)
        singleton = conf.get('singleton', True)
        with_constructor = conf.get('class', None)
        with_method = conf.get('init_method', None)
        with_function = conf.get('init_function', None)
        with_parameters = conf.get('init_parameters', [])
        post_creation = conf.get('post_creation', [])

        param = self._compute_params(with_parameters, service_prefix, variable_prefix)

        instance = None
        if with_constructor:
            module_name, class_name = with_constructor.rsplit('.', 1)
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            instance = class_(*param)
        elif with_method:
            module_name, class_name, method_name = with_method.rsplit('.', 2)
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            method = getattr(class_, method_name)
            instance = method(class_, *param)
        elif with_function:
            module_name, function_name = with_function.rsplit('.', 2)
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
            instance = function(*param)
        else:
            raise Exception ("Error no class for {}".format(service_name))

        for method_call in post_creation:
            method = method_call['method']
            module_name, class_name, method_name = method.rsplit('.', 2)
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            method = getattr(class_, method_name)
            parameters = method_call.get('parameters', [])
            param = self._compute_params(parameters, service_prefix, variable_prefix)
            method(instance, *param)

        if singleton is True:
            self._services[service_name] = instance

        return instance

    def _compute_params(self, parameters, object_prefix, variable_prefix):
        ret = []
        for par in parameters:
            if isinstance(par, str):
                if par[:len(object_prefix)] == object_prefix:
                    par = self._initService(par[len(object_prefix):])
                elif par[:len(variable_prefix)] == variable_prefix:
                    par = os.environ[par[len(variable_prefix):]]
            ret.append(par)
        return ret
#
