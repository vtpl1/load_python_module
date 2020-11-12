import unittest
from lopymo import load_python_module
class TestLoadPythonModule(unittest.TestCase):
    """
    docstring
    """
    def test_write_file(self):
        """
        docstring
        """
        x = load_python_module.LoadPythonModule()
        x.write_yaml()