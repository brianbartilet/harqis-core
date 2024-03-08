"""This conatins modules for JSON. Created for doing restful APIs with"""

import json
from collections import OrderedDict
from json import JSONDecodeError

import jsonpickle
from typing import TypeVar, Generic, Type, Union

from utilities.logging.custom_logger import custom_logger
log = custom_logger()
T = TypeVar('T')


def keys_exists(element: dict, *keys):
    """
    Check if *keys (nested) exists in `element` (dict).
    """
    if len(keys) == 0:
        raise AttributeError('No keys detected!')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except Exception:
            return None

    return _element


class JsonObject(Generic[T]):

    def __init__(self, *args, **kwargs):
        """This recreates the object from Json to a JsonObject"""

        if args is not None and len(args)>0 and isinstance(args[-1], dict):
            vars(self).update(args[-1])

        if kwargs.get('convert_kwargs'):
            for arg in kwargs:
                clean_chars = kwargs.get('clean_chars')
                try:
                    value = kwargs[arg]
                    if clean_chars is not None and type(value) is str:
                        for char in clean_chars:
                            value = value.replace(char, '')
                    kwargs[arg] = getattr(self, arg)(value)
                except:
                    continue

        self.__dict__.update(kwargs)

    def get_json(self):
        """This creates a json representation of the object"""
        return JsonUtil.serialize(self)

    def get_dict(self):
        s = JsonUtil.serialize(self)
        return JsonUtil.deserialize(s, type_hook=OrderedDict)


class JsonUtil(object):
    @staticmethod
    def serialize(obj):
        """Method for changing a class to a Json representation"""
        return jsonpickle.encode(obj, unpicklable=False)

    @staticmethod
    def deserialize(obj, type_hook : Type[T] = JsonObject[T], **kwargs) -> T:
        """Method for changing Json to a slightly strongly typed class"""
        try:
            return json.loads(obj, object_hook=type_hook, **kwargs)
        except JSONDecodeError:
            raise Exception("Could not decode data. Please check the JSON format.")

    @staticmethod
    def deserialize_from_dict(obj :  Union[OrderedDict, dict], type_hook : Type[T] = JsonObject[T]) -> T:
        # first dump
        raw_str = json.dumps(obj)
        return JsonUtil.deserialize(raw_str, type_hook)

    @staticmethod
    def deserialize_from_file(full_path, type_hook : Type[T] = JsonObject[T]) -> T:

        with open(full_path, "r") as obj:
            """Method for changing Json to a slightly strongly typed class"""
            return json.load(obj, object_hook=type_hook)