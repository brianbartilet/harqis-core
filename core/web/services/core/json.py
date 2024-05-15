"""This module contains utilities for working with JSON, primarily for webservice responses."""
import os
import json
import jsonpickle

from collections import OrderedDict
from json import JSONDecodeError
from typing import TypeVar, Generic, Type, Union

from core.utilities.logging.custom_logger import create_logger

log = create_logger()
TJsonObject = TypeVar('TJsonObject')
TResponse = TypeVar('TResponse')


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


def convert_to_jsonl(input_file_name: str,
                     input_base_path=os.getcwd(),
                     output_base_path=os.getcwd(),
                     text_key='text'):
    """
    Converts a text or JSON file to JSON Lines (JSONL) format.

    Args:
    - input_file_path: Path to the input file (either .txt or .json).
    - output_file_path: Path where the output .jsonl file will be saved.
    - text_key: The key to use for text lines in the output JSON objects (used for .txt files).

    """
    # Determine the type of the input file based on its extension
    input_file_path = os.path.join(input_base_path, input_file_name)
    file_extension = os.path.splitext(input_file_path)[-1].lower()

    output_file_path = os.path.join(output_base_path, f'{input_file_name.split(file_extension)[0]}.jsonl')
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file_path:

        if file_extension == '.txt':
            # Handle text files
            for line in input_file:
                line = line.strip()
                if line:  # Skip empty lines
                    json_obj = {text_key: line}
                    output_file_path.write(json.dumps(json_obj) + '\n')

        elif file_extension == '.json':
            # Handle JSON files containing an array of objects
            json_array = json.load(input_file)
            if isinstance(json_array, list):
                for obj in json_array:
                    output_file_path.write(json.dumps(obj) + '\n')
            else:
                raise ValueError("JSON input file must contain an array of objects.")

        else:
            for line in input_file:
                line = line.strip()
                if line:  # Skip empty lines
                    json_obj = {'content': line}
                    output_file_path.write(json.dumps(json_obj) + '\n')

    print(f"File converted to JSONL and saved to {output_file_path}")


class JsonObject(Generic[TJsonObject]):
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

        self.__dict__.update(kwargs)

    def get_json(self) -> str:
        """Converts the object to a JSON string."""
        return JsonUtility.serialize(self)

    def get_dict(self) -> dict:
        """Converts the object to a dictionary."""
        s = JsonUtility.serialize(self)
        return JsonUtility.deserialize(s, type_hook=OrderedDict)

    def sanitize(self, remove_characters: [] = None):
        """
        Sanitizes the attributes of the instance based on the specified configurations.

        This method iterates over each attribute stored in the instance, optionally
        removing specified characters from string values. It then attempts to convert
        each value to the original type of the attribute.

        Instance attributes are updated with their sanitized and converted values.

        Parameters:
            remove_characters (list, optional): A list of characters to remove from
            string values in the instance attributes. Defaults to None, which means
            no characters are removed.

        Raises:
            AttributeError: If an error occurs when trying to convert a value to a type,
            or if an attribute conversion fails.
        """
        for attr, value in vars(self).items():
            original_type = None
            try:
                if remove_characters is not None and isinstance(value, str):
                    for char in remove_characters:
                        value = value.replace(char, '')
                # Assuming that you want to keep the conversion to the original type
                original_type = type(getattr(self, attr))
                setattr(self, attr, original_type(value))
            except AttributeError:
                print(f"Cannot convert '{value}' from type '{original_type}'")
                continue


class JsonUtility:
    """A utility class for serializing and deserializing JSON."""

    @staticmethod
    def serialize(obj: TJsonObject) -> str:
        """
        Serializes an object to a JSON string.

        Args:
            obj (T): The object to serialize.

        Returns:
            A JSON string representation of the object.
        """
        return jsonpickle.encode(obj, unpicklable=False)

    @staticmethod
    def deserialize(obj: str, type_hook: Type[TResponse] = JsonObject[TJsonObject], **kwargs) -> TJsonObject:
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
    def deserialize_from_dict(obj: Union[OrderedDict, dict],
                              type_hook: Type[TResponse] = JsonObject[TJsonObject]) -> TJsonObject:
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
    def deserialize_from_file(full_path: str, type_hook: Type[TResponse] = JsonObject[TJsonObject]) -> TJsonObject:
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
