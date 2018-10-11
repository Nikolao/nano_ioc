#
import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import nano_ioc

class HelloWorld:
	def __init__(self, name):
		self.name = name

	def run(self):
		print("HelloWorld {}".format(self.name))

if __name__ == '__main__':
	with open("simple_demo.json") as file:
   		json_configuration = file.read()

	configuration = json.loads(json_configuration)

	container = nano_ioc.Container(configuration['services'])

	service = container.getService('hello-world')
	service.run()

#