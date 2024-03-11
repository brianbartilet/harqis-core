from typing import TypeVar, Type, cast

from utilities.data.json import JsonObject

T = TypeVar("T")


class BaseDto(JsonObject):

    message_return_code = ""
    message_status = ""
    message_return_description = ""
    data = None

    def __init__(self, *args):
        super(BaseDto, self).__init__(*args)

    # try again to deserialize the whole thing

    def get_deserialized_data(self, type_hook: Type[T]) -> T:
        return cast(type_hook, self.data)
