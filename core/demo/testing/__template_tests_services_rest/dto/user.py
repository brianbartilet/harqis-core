from core.web.services.core.json import JsonObject


class DtoUser(JsonObject):
    user_id: int = None
    id: int = None
    title: str = None
    body: str = None


class DtoUserTestCamel(JsonObject):
    userId: int = None
    title: str = None
    body: str = None
