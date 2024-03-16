import os.path
import unittest

from config.loader import ConfigLoader, Configuration


class UnitTestsConfigLoader(unittest.TestCase):
    def test_without_keywords(self):
        """Test loading configuration without specifying any additional keywords."""
        loader = ConfigLoader(Configuration.YAML)
        self.assertIsInstance(loader.config, dict)

    def test_override_path(self):
        """Test overriding the base path for the configuration file."""
        path = os.path.join(os.getcwd(), 'path/')
        loader = ConfigLoader(Configuration.YAML, base_path=path)
        self.assertIsInstance(loader.config, dict)

    def test_override_path_yaml(self):
        """Test loading a YAML configuration file by specifying the file name."""
        file = 'data.yaml'
        loader = ConfigLoader(Configuration.YAML, file_name=file)
        self.assertIsInstance(loader.config, dict)

    def test_override_path_yaml_without_file_extension(self):
        """Test loading a YAML configuration file by specifying the file name."""
        file = 'data'
        loader = ConfigLoader(Configuration.YAML, file_name=file)
        self.assertIsInstance(loader.config, dict)

    def test_override_path_yaml_fail(self):
        """Test loading a non-existent YAML configuration file, expecting a SystemExit exception."""
        with self.assertRaises(FileNotFoundError):
            file = 'invalid.yaml'
            loader = ConfigLoader(Configuration.YAML, file_name=file)
            loader.config()

    def test_override_path_json(self):
        """Test loading a JSON configuration file by specifying the file name."""
        file = 'data.json'
        loader = ConfigLoader(Configuration.JSON, file_name=file)
        self.assertIsInstance(loader.config, dict)

    def test_override_path_json_fail(self):
        """Test loading a non-existent JSON configuration file, expecting a SystemExit exception."""
        with self.assertRaises(FileNotFoundError):
            file = 'invalid.json'
            loader = ConfigLoader(Configuration.JSON, file_name=file)
            loader.config()
