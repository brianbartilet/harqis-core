from core.web.services.core.json import JsonObject


class User(JsonObject):
    user_id: int = None
    id: int = None
    title: str = None
    body: str = None


class UserTestCamel(JsonObject):
    userId: int = None
    title: str = None
    body: str = None
