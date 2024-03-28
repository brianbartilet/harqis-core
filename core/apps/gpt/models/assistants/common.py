from core.web.services.core.json import JsonObject
from typing import Optional


class ListQuery(JsonObject):
    """
    Model for a List.
    """
    limit: int = 20  # The maximum number of items to return in the list. Default is 20.
    order: str = 'desc'  # The order in which to sort the items in the list. Default is 'desc'.
    after: str = None  # A cursor for use in pagination. `after` is an item id that defines your place in the list.
    before: str = None  # A cursor for use in pagination. `before` is an item id that defines your place in the list.


class ListResponse(JsonObject):
    object: str = None  # The type of the object, should be "list_response".
    data: list = None  # A list of Models in the response.
    first_id: str = None  # The ID of the first item in the list.
    last_id: str = None  # The ID of the last item in the list.
    has_more: bool = False  # A flag indicating if there are more items to fetch.


class ResponseStatus(JsonObject):
    id: str = None  # The unique identifier for the response.
    object: str = None  # Target object with operation
    deleted: bool = False  # A flag indicating if the object was deleted.
    created: bool = False  # A flag indicating if the object was created.
    updated: bool = False  # A flag indicating if the object was updated.
    deleted_at: int = None  # The timestamp of when the object was deleted.
    created_at: int = None  # The timestamp of when the object was created.
    updated_at: int = None  # The timestamp of when the object was updated.
    metadata: Optional = None  # T metadata associated with the message.


class Error(JsonObject):
    code: str = None  # The error code.
    message: str = None  # The error message.
