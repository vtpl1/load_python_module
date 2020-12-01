import yaml
# http://su0.io/2020/08/05/python-strict-yaml-deserialization.html
from pprint import pprint

from yaml import load, SafeLoader
from marshmallow_dataclass import class_schema

class LoadPythonModule():
    def __init__(self):
        self.__file_name = "app.yaml"
        pass

    def read_yaml(self):
        pass

    def write_yaml(self):
        pass
