import unittest
from unittest.mock import patch
from utilities.resources.loader import ResourceDataLoader, Resource

class TestResourceDataLoader(unittest.TestCase):
    def setUp(self):
        self.gql_mutation = 'mutation.gql'
        self.gql_query = 'query.gql'
        self.base_path = 'path'

    @patch('utilities.resources.loader.ResourceFileGql.load')
    @patch('utilities.resources.loader.ResourceFileGql.find_file_from_base_path')
    def test_gql_loader_success(self, mock_find_file, mock_load):
        mock_find_file.return_value = '/path/to/resources/test_data.gql'
        mock_load.return_value = 'query { test }'

        loader = ResourceDataLoader(Resource.GQL, 'test_data.gql', self.base_path)
        data = loader.data

        self.assertEqual(data, 'query { test }')
        mock_load.assert_called_once()

    def test_gql_loader_success_file_query(self):
        loader = ResourceDataLoader(Resource.GQL, self.gql_query, self.base_path)
        data = loader.data
        self.assertIn('query', data)
        self.assertIn('variables', data)

    def test_gql_loader_success_file_query_with_variables(self):
        class MockedClass:
            def __init__(self):
                self.value = 100
        dto = MockedClass()
        loader = ResourceDataLoader(Resource.GQL, self.gql_query, self.base_path, variables=dto)
        data = loader.data
        self.assertIn('value', data['variables'])