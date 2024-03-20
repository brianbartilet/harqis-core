import unittest
import os
from core.utilities.resources.types.json_schema import ResourceFileJsonSchema


class TestResourceFileJsonSchema(unittest.TestCase):
    def setUp(self):
        # Assuming there is a valid schema file 'test_schema.json' in the test directory
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
        self.schema_loader = ResourceFileJsonSchema(file_name='schema.json', base_path=self.path)

    def test_load_schema(self):
        schema = self.schema_loader.load()
        self.assertIsInstance(schema, dict)

    def test_validate_valid_data(self):
        # Assuming the schema expects an object with an integer 'id', a string 'name', and an integer 'age'
        valid_data = {'id': 123, 'name': 'John Doe', 'age': 30}
        result = self.schema_loader.validate(valid_data)
        self.assertTrue(result)

    def test_validate_invalid_data(self):
        # Assuming the schema expects an object with an integer 'id'
        invalid_data = {'id': 'not an integer'}
        result = self.schema_loader.validate(invalid_data)
        self.assertFalse(result)

    def test_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            non_existent_loader = ResourceFileJsonSchema(file_name='non_existent.json', base_path=self.path)
            non_existent_loader.load()
