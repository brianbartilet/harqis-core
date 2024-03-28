import unittest
from core.utilities.data.objects import *


class UnitTestsObjectUtilities(unittest.TestCase):
    def test_convert_to_snake_case(self):
        """Test converting strings from camelCase and PascalCase to snake_case."""
        self.assertEqual(convert_to_snake_case('camelCase'), 'camel_case')
        self.assertEqual(convert_to_snake_case('PascalCase'), 'pascal_case')
        self.assertEqual(convert_to_snake_case('snake_case'), 'snake_case')

    def test_convert_dictionary_keys_to_snake_case(self):
        """Test converting dictionary keys in an object to snake_case."""
        class TestObject:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        obj = TestObject(camelCaseKey=1, PascalCaseKey=2)
        converted_obj = convert_dict_keys_to_snake(obj)

        self.assertTrue(hasattr(converted_obj, 'camel_case_key'))
        self.assertTrue(hasattr(converted_obj, 'pascal_case_key'))
        self.assertFalse(hasattr(converted_obj, 'camelCaseKey'))
        self.assertFalse(hasattr(converted_obj, 'PascalCaseKey'))

    def test_convert_object_list_to_snake_case(self):
        """Test converting a list of objects with dictionary keys to snake_case."""
        class TestObject:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        obj_list = [TestObject(camelCaseKey=1, PascalCaseKey=2), TestObject(camelCaseKey=3, PascalCaseKey=4)]
        converted_list = convert_objects_to_snake(obj_list)

        for obj in converted_list:
            self.assertTrue(hasattr(obj, 'camel_case_key'))
            self.assertTrue(hasattr(obj, 'pascal_case_key'))
            self.assertFalse(hasattr(obj, 'camelCaseKey'))
            self.assertFalse(hasattr(obj, 'PascalCaseKey'))

    def test_convert_object_keys_to_snake_case(self):
        """Test converting keys of an object or a list of objects to snake_case."""
        class TestObject:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        obj = TestObject(camelCaseKey=1, PascalCaseKey=2)
        converted_obj = convert_object_keys_to_snake(obj)

        self.assertTrue(hasattr(converted_obj, 'camel_case_key'))
        self.assertTrue(hasattr(converted_obj, 'pascal_case_key'))
        self.assertFalse(hasattr(converted_obj, 'camelCaseKey'))
        self.assertFalse(hasattr(converted_obj, 'PascalCaseKey'))

        obj_list = [TestObject(camelCaseKey=1, PascalCaseKey=2), TestObject(camelCaseKey=3, PascalCaseKey=4)]
        converted_list = convert_object_keys_to_snake(obj_list)

        for obj in converted_list:
            self.assertTrue(hasattr(obj, 'camel_case_key'))
            self.assertTrue(hasattr(obj, 'pascal_case_key'))
            self.assertFalse(hasattr(obj, 'camelCaseKey'))
            self.assertFalse(hasattr(obj, 'PascalCaseKey'))

    def test_convert_object_list(self):
        """Test converting a list of objects from one type to another."""
        class SourceObject:
            def __init__(self, key1, key2):
                self.key1 = key1
                self.key2 = key2

        class TargetObject:
            def __init__(self, key1, key2):
                self.key1 = key1
                self.key2 = key2

        obj_list = [SourceObject(key1=1, key2=2), SourceObject(key1=3, key2=4)]
        converted_list = convert_object_list(obj_list, TargetObject)

        self.assertIsInstance(converted_list[0], TargetObject)
        self.assertIsInstance(converted_list[1], TargetObject)
        self.assertEqual(converted_list[0].key1, 1)
        self.assertEqual(converted_list[0].key2, 2)
        self.assertEqual(converted_list[1].key1, 3)
        self.assertEqual(converted_list[1].key2, 4)
