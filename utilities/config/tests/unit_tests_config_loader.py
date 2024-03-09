import os.path
import unittest, pytest

from utilities.config.loader import ConfigLoader, Configuration

class UnitTestsConfigLoader(unittest.TestCase):
    def test_without_keywords(self):
        loader = ConfigLoader(Configuration.YAML)
        data = loader.load()
        assert (isinstance(data, dict), True)

    def test_override_path(self):
        path = os.path.join(os.getcwd(), 'location')
        loader = ConfigLoader(Configuration.YAML, base_path=path)
        data = loader.load()
        assert (isinstance(data, dict), True)

    def test_override_path_yaml(self):
        file = 'data.yaml'
        loader = ConfigLoader(Configuration.YAML, name=file)
        data = loader.load()
        assert (isinstance(data, dict), True)

    def test_override_path_yaml_fail(self):
        with pytest.raises(SystemExit):
            file = 'invalid.yaml'
            loader = ConfigLoader(Configuration.YAML, name=file)
            loader.load()

    def test_override_path_json(self):
        file = 'data.json'
        loader = ConfigLoader(Configuration.JSON, name=file)
        data = loader.load()
        assert (isinstance(data, dict), True)

    def test_override_path_json_fail(self):
        with pytest.raises(SystemExit):
            file = 'invalid.json'
            loader = ConfigLoader(Configuration.JSON, name=file)
            loader.load()
