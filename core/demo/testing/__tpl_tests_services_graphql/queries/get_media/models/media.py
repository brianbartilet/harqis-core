from core.web.services.core.json import JsonObject


class Title(JsonObject):
    romaji: str = None
    english: str = None
    native: str = None


class Media(JsonObject):
    id: int = None
    title: Title = None

