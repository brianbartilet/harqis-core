import re
from typing import Type, TypeVar, List

T = TypeVar('T')


class ObjectUtils:
    @staticmethod
    def convert_dict_keys_to_snake(cur_object: T) -> T:
        """
        Convert the keys of a dictionary representing an object's attributes to snake_case.

        Args:
            cur_object: The object whose attributes need to be converted.

        Returns:
            A new object with attributes in snake_case.
        """
        object_type = type(cur_object)
        obj_dict = cur_object.__dict__
        for key, value in obj_dict.copy().items():
            snake_case_key = ObjectUtils.convert_to_snake_case(key)
            if snake_case_key != key:
                obj_dict[snake_case_key] = obj_dict.pop(key)
        new_obj = object_type(**obj_dict)
        return new_obj

    @staticmethod
    def convert_objects_to_snake(object_collection: List[T]) -> List[T]:
        """
        Convert the keys of dictionaries representing a list of objects' attributes to snake_case.

        Args:
            object_collection: The list of objects whose attributes need to be converted.

        Returns:
            A new list of objects with attributes in snake_case.
        """
        return [ObjectUtils.convert_dict_keys_to_snake(item) for item in object_collection]

    @staticmethod
    def convert_object_keys_to_snake(object_item: T) -> T:
        """
        Convert the keys of a dictionary or a list of dictionaries representing an object's or objects' attributes to snake_case.

        Args:
            object_item: The object or list of objects whose attributes need to be converted.

        Returns:
            The object or list of objects with attributes in snake_case.
        """
        if isinstance(object_item, list):
            return ObjectUtils.convert_objects_to_snake(object_item)
        else:
            return ObjectUtils.convert_dict_keys_to_snake(object_item)

    @staticmethod
    def convert_object_list(object_collection: List, object_type: Type[T]) -> List[T]:
        """
        Convert a list of objects to a new list of objects of a specific type.

        Args:
            object_collection: The list of objects to be converted.
            object_type: The new type of objects.

        Returns:
            A new list of objects of the specified type.
        """
        return [object_type(**item.__dict__) for item in object_collection]

    @staticmethod
    def convert_to_snake_case(stream: str) -> str:
        """
        Convert a given text from camelCase or PascalCase to snake_case.

        Args:
            stream: The text to be converted.

        Returns:
            The text in snake_case.
        """
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', stream)
        return '_'.join(word.lower() for word in words)