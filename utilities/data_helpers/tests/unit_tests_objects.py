import unittest
from utilities.data_helpers.objects import ObjectUtilities


class UnitTestsObjectUtilities(unittest.TestCase):

    def test_convert_to_snake_case(self):
        self.assertEqual(ObjectUtilities.convert_to_snake_case('camelCase'), 'camel_case')
        self.assertEqual(ObjectUtilities.convert_to_snake_case('PascalCase'), 'pascal_case')
        self.assertEqual(ObjectUtilities.convert_to_snake_case('snake_case'), 'snake_case')

    def test_convert_dictionary_keys_to_snake_case(self):
        class TestObject:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        obj = TestObject(camelCaseKey=1, PascalCaseKey=2)
        converted_obj = ObjectUtilities.convert_dictionary_keys_to_snake_case(obj)

        self.assertTrue(hasattr(converted_obj, 'camel_case_key'))
        self.assertTrue(hasattr(converted_obj, 'pascal_case_key'))
        self.assertFalse(hasattr(converted_obj, 'camelCaseKey'))
        self.assertFalse(hasattr(converted_obj, 'PascalCaseKey'))

    def test_convert_object_list_to_snake_case(self):
        class TestObject:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        obj_list = [TestObject(camelCaseKey=1, PascalCaseKey=2), TestObject(camelCaseKey=3, PascalCaseKey=4)]
        converted_list = ObjectUtilities.convert_object_list_to_snake_case(obj_list)

        for obj in converted_list:
            self.assertTrue(hasattr(obj, 'camel_case_key'))
            self.assertTrue(hasattr(obj, 'pascal_case_key'))
            self.assertFalse(hasattr(obj, 'camelCaseKey'))
            self.assertFalse(hasattr(obj, 'PascalCaseKey'))

    def test_convert_object_keys_to_snake_case(self):
        class TestObject:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        obj = TestObject(camelCaseKey=1, PascalCaseKey=2)
        converted_obj = ObjectUtilities.convert_object_keys_to_snake_case(obj)

        self.assertTrue(hasattr(converted_obj, 'camel_case_key'))
        self.assertTrue(hasattr(converted_obj, 'pascal_case_key'))
        self.assertFalse(hasattr(converted_obj, 'camelCaseKey'))
        self.assertFalse(hasattr(converted_obj, 'PascalCaseKey'))

        obj_list = [TestObject(camelCaseKey=1, PascalCaseKey=2), TestObject(camelCaseKey=3, PascalCaseKey=4)]
        converted_list = ObjectUtilities.convert_object_keys_to_snake_case(obj_list)

        for obj in converted_list:
            self.assertTrue(hasattr(obj, 'camel_case_key'))
            self.assertTrue(hasattr(obj, 'pascal_case_key'))
            self.assertFalse(hasattr(obj, 'camelCaseKey'))
            self.assertFalse(hasattr(obj, 'PascalCaseKey'))

    def test_convert_object_list(self):
        class SourceObject:
            def __init__(self, key1, key2):
                self.key1 = key1
                self.key2 = key2

        class TargetObject:
            def __init__(self, key1, key2):
                self.key1 = key1
                self.key2 = key2

        obj_list = [SourceObject(key1=1, key2=2), SourceObject(key1=3, key2=4)]
        converted_list = ObjectUtilities.convert_object_list(obj_list, TargetObject)

        self.assertIsInstance(converted_list[0], TargetObject)
        self.assertIsInstance(converted_list[1], TargetObject)
        self.assertEqual(converted_list[0].key1, 1)
        self.assertEqual(converted_list[0].key2, 2)
        self.assertEqual(converted_list[1].key1, 3)
        self.assertEqual(converted_list[1].key2, 4)