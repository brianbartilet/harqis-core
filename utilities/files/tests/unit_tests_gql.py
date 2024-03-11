import unittest
from pathlib import Path
from utilities.web.services.gql import FilesSetup, read_file, parse_gql_file, is_json, safe_json_parse


class TestGraphqlUtils(unittest.TestCase):

    def setUp(self):
        # Set up the test environment
        self.test_file_path = Path(FilesSetup.get_instance().config_dir, "test.txt")
        self.test_gql_path = Path(FilesSetup.get_instance().config_dir, "test.gql")
        self.test_file_content = "Hello, World!"
        self.test_gql_content = "query { test }"

        # Create test files
        self.test_file_path.write_text(self.test_file_content)
        self.test_gql_path.write_text(self.test_gql_content)

    def tearDown(self):
        # Clean up test files
        self.test_file_path.unlink()
        self.test_gql_path.unlink()

    def test_read_file(self):
        # Test reading a file
        content = read_file("test.txt")
        self.assertEqual(content, self.test_file_content)

    def test_parse_gql_file(self):
        # Test parsing a GraphQL file
        result = parse_gql_file("test.gql")
        self.assertEqual(result, {"query": self.test_gql_content, "variables": None})

    def test_is_json(self):
        # Test checking if a string is valid JSON
        self.assertTrue(is_json('{"key": "value"}'))
        self.assertFalse(is_json('not a json string'))

    def test_safe_json_parse(self):
        # Test safely parsing JSON
        self.assertEqual(safe_json_parse('{"key": "value"}'), {"key": "value"})
        self.assertEqual(safe_json_parse('not a json string'), 'not a json string')


if __name__ == '__main__':
    unittest.main()
