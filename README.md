
# Nano IOC - Lightweight Inversion Of Control framework

## Description

The main objective is to have the lightest framework possible.

- no config file management
- no dependancies

but as many features as possible

- singleton services
- multi instance services
- all kind of class creation
    - class init method
    - class static method
    - function
- post creation set of methods
- all methods/functions accept
    - parameters of all kind
    - instances of services as parameters 
    - env variables as parameters
- configurable syntax for
    - instances of services
    - environment variables

in less than 100 lines.


### Exemple


```
import nano_ioc


class HelloWorld:
    def __init__(self, name):
        self.name = name

    def run(self):
        print("HelloWorld {}".format(self.name))


if __name__ == '__main__':

    configuration = {
        'hello-world': {
		"class": "HelloWorld",
		"init_parameters": ["Bob"]
        }
    }
    container = nano_ioc.Container(configuration)

    service = container.getService('hello-world')
    service.run()
```

Result
```
HelloWorld Bob
```

## configuration parameter


### top level attributes

- service_prefix: the prefix for instances of services as parameters ('@' by default)
- variable_prefix: the prefix for environment variables as parameters ('$' by default)
- services: the dictionary of declared services.


### description of a service

- create-at-init: if True will be created at Container creation, else will be created at first demand (False by default)
- singleton: if True a new object will be created each time (False by default)


### creation of a service

- class: full class name, the service will be created using the init method
- init_method: full method name used to create the service
- init_function: full function name, used to create the service
- init_parameters: list of parameters for init method/function (empty by default)


### configuration of a service

- post_creation: a list of method call description, executed after the creation of the service (empty by default)

Each post creation method call description contain:

- method: full method name
- parameters: list of parameters for the method (empty by default)



## About parameters

Method/function parameters can be of any type.

The Container considers parameters starting with the service_prefix as service names

ex: '@service1' will be replaced by the object created for the service named 'service1'

The Container considers parameters starting with the env_variable_prefix as environment variables

ex: '$USER' will be replaced by the value of the USER environment variable.



## References and components used

- https://media.readthedocs.org/pdf/python-guide/latest/python-guide.pdf
- https://www.fullstackpython.com/


- https://www.conventionalcommits.org/en/v1.0.0-beta.2/
- https://keepachangelog.com/en/1.0.0/
- https://semver.org/
- https://www.makeareadme.com/


- python3 : https://www.python.org/
- pypi : https://pypi.org/
- pytest : https://docs.pytest.org/en/latest/
- black : https://github.com/ambv/black
- flake8 : https://pypi.org/project/flake8/
- pre-commit : https://pre-commit.com/
- gcloud
