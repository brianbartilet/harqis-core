import re

class ObjectUtilities:
    @staticmethod
    def convert_dictionary_keys_to_snake_case(cur_object=None):
        """
        Convert the keys of a dictionary representing an object's attributes to snake_case.

        :param cur_object: The object whose attributes need to be converted.
        :return: A new object with attributes in snake_case.
        """
        object_type = type(cur_object)
        obj_dict = cur_object.__dict__
        for key, value in obj_dict.copy().items():
            snake_case_key = ObjectUtilities.convert_to_snake_case(key)
            if snake_case_key != key:
                obj_dict[snake_case_key] = obj_dict.pop(key)
        new_obj = object_type(**obj_dict)
        return new_obj

    @staticmethod
    def convert_object_list_to_snake_case(object_collection=None):
        """
        Convert the keys of dictionaries representing a list of objects' attributes to snake_case.

        :param object_collection: The list of objects whose attributes need to be converted.
        :return: A new list of objects with attributes in snake_case.
        """
        return [ObjectUtilities.convert_dictionary_keys_to_snake_case(item) for item in object_collection]

    @staticmethod
    def convert_object_keys_to_snake_case(object_item=None):
        """
        Convert the keys of a dictionary or a list of dictionaries representing an object's or objects' attributes to snake_case.

        :param object_item: The object or list of objects whose attributes need to be converted.
        :return: The object or list of objects with attributes in snake_case.
        """
        try:
            if isinstance(object_item, list):
                return ObjectUtilities.convert_object_list_to_snake_case(object_item)
            else:
                return ObjectUtilities.convert_dictionary_keys_to_snake_case(object_item)
        except Exception as e:
            # Log the error if necessary
            return object_item

    @staticmethod
    def convert_object_list(object_collection=None, object_type=None):
        """
        Convert a list of objects to a new list of objects of a specific type.

        :param object_collection: The list of objects to be converted.
        :param object_type: The new type of objects.
        :return: A new list of objects of the specified type.
        """
        return [object_type(**item.__dict__) for item in object_collection]

    @staticmethod
    def convert_to_snake_case(text):
        """
        Convert a given text from camelCase or PascalCase to snake_case.

        :param text: The text to be converted.
        :return: The text in snake_case.
        """
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', text)
        return '_'.join(map(str.lower, words))
