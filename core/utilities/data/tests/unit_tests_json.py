import unittest
from core.web.services.core.json import JsonObject, JsonUtility, keys_exists
import os


class TestJsonObject(unittest.TestCase):
    """Tests for the JsonObject class."""

    def test_get_json(self):
        """Test that get_json() returns the correct JSON representation of the object."""
        obj = JsonObject(name="John", age=30)
        json_str = obj.get_json()
        self.assertEqual(json_str, '{"name": "John", "age": 30}')

    def test_get_dict(self):
        """Test that get_dict() returns the correct dictionary representation of the object."""
        obj = JsonObject(name="John", age=30)
        obj_dict = obj.get_dict()
        self.assertEqual(obj_dict, {"name": "John", "age": 30})


class TestJsonUtil(unittest.TestCase):
    """Tests for the JsonUtil class."""

    def test_serialize(self):
        """Test that serialize() correctly converts an object to a JSON string."""
        obj = JsonObject(name="John", age=30)
        json_str = JsonUtility.serialize(obj)
        self.assertEqual(json_str, '{"name": "John", "age": 30}')

    def test_deserialize(self):
        """Test that deserialize() correctly converts a JSON string to an object."""
        json_str = '{"name": "John", "age": 30}'
        obj = JsonUtility.deserialize(json_str)
        self.assertEqual(obj.name, "John")
        self.assertEqual(obj.age, 30)

    def test_deserialize_from_dict(self):
        """Test that deserialize_from_dict() correctly converts a dictionary to an object."""
        obj_dict = {"name": "John", "age": 30}
        obj = JsonUtility.deserialize_from_dict(obj_dict)
        self.assertEqual(obj.name, "John")
        self.assertEqual(obj.age, 30)

    def test_deserialize_from_file(self):
        """Test that deserialize_from_file() correctly reads a JSON file and converts it to an object."""
        # Create a temporary JSON file
        file_path = 'temp.json'
        with open(file_path, 'w') as f:
            f.write('{"name": "John", "age": 30}')

        obj = JsonUtility.deserialize_from_file(file_path)
        os.remove(file_path)  # Clean up the temporary file
        self.assertEqual(obj.name, "John")
        self.assertEqual(obj.age, 30)


class TestKeysExists(unittest.TestCase):
    """Tests for the keys_exists() function."""

    def test_keys_exists(self):
        """Test that keys_exists() correctly checks if nested keys exist in a dictionary."""
        test_dict = {"a": {"b": {"c": "d"}}}
        self.assertEqual(keys_exists(test_dict, "a", "b", "c"), "d")
        self.assertIsNone(keys_exists(test_dict, "a", "b", "x"))
        self.assertIsNone(keys_exists(test_dict, "x"))