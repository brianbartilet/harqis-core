from core.web.services.core.json import JsonObject


class DtoPostPayload(JsonObject):
    title: str = None
    body: str = None
    userId: int = None


