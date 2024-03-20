import os.path
import unittest

from core.config.loader import ConfigFileLoader, ConfigFile


class UnitTestsConfigLoader(unittest.TestCase):

    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_without_keywords(self):
        """Test loading configuration without specifying any additional keywords."""
        loader = ConfigFileLoader(ConfigFile.YAML, base_path=self.path)
        self.assertIsInstance(loader.config, dict)

    def test_override_path(self):
        """Test overriding the base path for the configuration file."""
        loader = ConfigFileLoader(ConfigFile.YAML, base_path=self.path)
        self.assertIsInstance(loader.config, dict)

    def test_override_path_yaml(self):
        """Test loading a YAML configuration file by specifying the file name."""
        file = 'data.yaml'
        loader = ConfigFileLoader(ConfigFile.YAML, file_name=file, base_path=self.path)
        self.assertIsInstance(loader.config, dict)

    def test_override_path_yaml_without_file_extension(self):
        """Test loading a YAML configuration file by specifying the file name."""
        file = 'data'
        loader = ConfigFileLoader(ConfigFile.YAML, file_name=file, base_path=self.path)
        self.assertIsInstance(loader.config, dict)

    def test_override_path_yaml_fail(self):
        """Test loading a non-existent YAML configuration file, expecting a SystemExit exception."""
        with self.assertRaises(FileNotFoundError):
            file = 'invalid.yaml'
            loader = ConfigFileLoader(ConfigFile.YAML, file_name=file, base_path=self.path)
            loader.config()

    def test_override_path_json(self):
        """Test loading a JSON configuration file by specifying the file name."""
        file = 'data.json'
        loader = ConfigFileLoader(ConfigFile.JSON, file_name=file, base_path=self.path)
        self.assertIsInstance(loader.config, dict)

    def test_override_path_json_fail(self):
        """Test loading a non-existent JSON configuration file, expecting a SystemExit exception."""
        with self.assertRaises(FileNotFoundError):
            file = 'invalid.json'
            loader = ConfigFileLoader(ConfigFile.JSON, file_name=file, base_path=self.path)
            loader.config()
