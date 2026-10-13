#
import os
import importlib

try:
    string_types = (basestring,)
except NameError:  # Python 3
    string_types = (str,)


class Container:
    def __init__(self, configuration, debug=False):
        if not isinstance(configuration, dict):
            raise TypeError("configuration must be a dictionary")

        self._debug = debug
        self._configuration = configuration
        self._services = {}

        services = self._configuration.get("services", {})
        if not isinstance(services, dict):
            raise TypeError("configuration['services'] must be a dictionary")

        for service_name in services:
            conf = services[service_name]
            if not isinstance(conf, dict):
                raise TypeError(
                    "configuration['services'][{!r}] must be a dictionary".format(
                        service_name
                    )
                )
            create = conf.get("create-at-init", False)
            if create:
                self._initService(service_name)

    def getService(self, service_name):
        if service_name not in self._services:
            return self._initService(service_name)
        return self._services[service_name]

    def _initService(self, service_name):
        if service_name in self._services:
            return self._services[service_name]

        service_prefix = self._configuration.get("service_prefix", "@")
        variable_prefix = self._configuration.get("variable_prefix", "$")

        services = self._configuration.get("services", {})
        if service_name not in services:
            raise KeyError("Service '{}' is not configured".format(service_name))

        conf = services[service_name]
        singleton = conf.get("singleton", True)
        with_constructor = conf.get("class", None)
        with_method = conf.get("init_method", None)
        with_function = conf.get("init_function", None)
        with_parameters = conf.get("init_parameters", [])
        post_creation = conf.get("post_creation", [])

        param = self._compute_params(with_parameters, service_prefix, variable_prefix)

        instance = None
        if with_constructor:
            try:
                module_name, class_name = with_constructor.rsplit(".", 1)
            except ValueError:
                raise ValueError(
                    "Invalid class path '{}' for service '{}'".format(
                        with_constructor, service_name
                    )
                )
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            instance = class_(*param)
        elif with_method:
            try:
                module_name, class_name, method_name = with_method.rsplit(".", 2)
            except ValueError:
                raise ValueError(
                    "Invalid init_method '{}' for service '{}'".format(
                        with_method, service_name
                    )
                )
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            method = getattr(class_, method_name)
            instance = method(class_, *param)
        elif with_function:
            try:
                module_name, function_name = with_function.rsplit(".", 1)
            except ValueError:
                raise ValueError(
                    "Invalid init_function '{}' for service '{}'".format(
                        with_function, service_name
                    )
                )
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
            instance = function(*param)
        else:
            raise Exception("Error no class for {}".format(service_name))

        for method_call in post_creation:
            if not isinstance(method_call, dict):
                raise TypeError(
                    "post_creation entry for service '{}' must be a dictionary".format(
                        service_name
                    )
                )
            method = method_call["method"]
            try:
                module_name, class_name, method_name = method.rsplit(".", 2)
            except ValueError:
                raise ValueError(
                    "Invalid post_creation method '{}' for service '{}'".format(
                        method, service_name
                    )
                )
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            method = getattr(class_, method_name)
            parameters = method_call.get("parameters", [])
            param = self._compute_params(parameters, service_prefix, variable_prefix)
            method(instance, *param)

        if singleton is True:
            self._services[service_name] = instance

        return instance

    def _compute_params(self, parameters, object_prefix, variable_prefix):
        ret = []
        for par in parameters:
            if isinstance(par, string_types):
                if par.startswith(object_prefix):
                    if len(par) == len(object_prefix):
                        raise ValueError("Missing service name after prefix '{}'".format(object_prefix))
                    par = self._initService(par[len(object_prefix):])
                elif par.startswith(variable_prefix):
                    env_name = par[len(variable_prefix):]
                    if not env_name:
                        raise ValueError("Missing environment variable name after prefix '{}'".format(variable_prefix))
                    if env_name not in os.environ:
                        raise KeyError(
                            "Environment variable '{}' is not set".format(env_name)
                        )
                    par = os.environ[env_name]
            ret.append(par)
        return ret


#
