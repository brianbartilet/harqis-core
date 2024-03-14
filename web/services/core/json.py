"""This module contains utilities for working with JSON, primarily for webservice responses."""
import json
import jsonpickle

from collections import OrderedDict
from json import JSONDecodeError
from typing import TypeVar, Generic, Type, Union

from utilities.logging.custom_logger import create_logger

log = create_logger()
T = TypeVar('T')


def keys_exists(element: dict, *keys) -> Union[None, dict]:
    """
    Check if a nested sequence of keys exists in a given dictionary.

    Args:
        element (dict): The dictionary to check.
        *keys: A sequence of keys to check for.

    Returns:
        The value corresponding to the nested keys if they exist, otherwise None.
    """
    if len(keys) == 0:
        raise AttributeError('No keys detected!')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return None

    return _element


class JsonObject(Generic[T]):
    """
    A class for creating objects from JSON and converting objects to JSON.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the JsonObject class.

        Args:
            *args: Optional arguments that can be used to initialize the object.
            **kwargs: Optional keyword arguments that can be used to initialize the object.
        """
        if args is not None and len(args) > 0 and isinstance(args[-1], dict):
            vars(self).update(args[-1])

        if kwargs.get('convert_kwargs'):
            for arg in kwargs:
                clean_chars = kwargs.get('clean_chars')
                try:
                    value = kwargs[arg]
                    if clean_chars is not None and isinstance(value, str):
                        for char in clean_chars:
                            value = value.replace(char, '')
                    kwargs[arg] = getattr(self, arg)(value)
                except AttributeError:
                    continue

        self.__dict__.update(kwargs)

    def get_json(self) -> str:
        """Converts the object to a JSON string."""
        return JsonUtility.serialize(self)

    def get_dict(self) -> dict:
        """Converts the object to a dictionary."""
        s = JsonUtility.serialize(self)
        return JsonUtility.deserialize(s, type_hook=OrderedDict)


class JsonUtility:
    """A utility class for serializing and deserializing JSON."""

    @staticmethod
    def serialize(obj: T) -> str:
        """
        Serializes an object to a JSON string.

        Args:
            obj (T): The object to serialize.

        Returns:
            A JSON string representation of the object.
        """
        return jsonpickle.encode(obj, unpicklable=False)

    @staticmethod
    def deserialize(obj: str, type_hook: Type[T] = JsonObject[T], **kwargs) -> T:
        """
        Deserializes a JSON string to an object.

        Args:
            obj (str): The JSON string to deserialize.
            type_hook (Type[T]): The type of the object to deserialize to.

        Returns:
            An object of the specified type.

        Raises:
            JSONDecodeError: If the JSON string cannot be decoded.
        """
        try:
            return json.loads(obj, object_hook=type_hook, **kwargs)
        except JSONDecodeError:
            raise Exception("Could not decode data. Please check the JSON format.")

    @staticmethod
    def deserialize_from_dict(obj: Union[OrderedDict, dict], type_hook: Type[T] = JsonObject[T]) -> T:
        """
        Deserializes a dictionary to an object.

        Args:
            obj (Union[OrderedDict, dict]): The dictionary to deserialize.
            type_hook (Type[T]): The type of the object to deserialize to.

        Returns:
            An object of the specified type.
        """
        raw_str = json.dumps(obj)
        return JsonUtility.deserialize(raw_str, type_hook)

    @staticmethod
    def deserialize_from_file(full_path: str, type_hook: Type[T] = JsonObject[T]) -> T:
        """
        Deserializes a JSON file to an object.

        Args:
            full_path (str): The path to the JSON file.
            type_hook (Type[T]): The type of the object to deserialize to.

        Returns:
            An object of the specified type.
        """
        with open(full_path, "r") as obj:
            return json.load(obj, object_hook=type_hook)
