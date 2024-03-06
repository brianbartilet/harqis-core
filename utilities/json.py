import json
from collections import OrderedDict

import jsonpickle
from typing import TypeVar, Generic, Type, Union

T = TypeVar('T')

class JsonObject(Generic[T]):

    def __init__(self, *args ):
        """This recreates the object from Json to a JsonObject"""

        if args is not None and len(args) > 0 and isinstance(args[-1], dict):
            vars(self).update(args[-1])

    def get_json(self):
        """This creates a json representation of the object"""
        return JsonUtil.serialize(self)

    def get_dict(self):
        s =JsonUtil.serialize(self)
        return JsonUtil.deserialize(s, type_hook=OrderedDict)

class JsonUtil(object):
    @staticmethod
    def serialize(obj):
        """Method for changing a class to a Json representation"""
        return jsonpickle.encode(obj, unpicklable=False)

    @staticmethod
    def deserialize(obj, type_hook : Type[T] = JsonObject[T]) -> T:
        """Method for changing Json to a slightly strongly typed class"""
        return json.loads(obj, object_hook=type_hook)

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