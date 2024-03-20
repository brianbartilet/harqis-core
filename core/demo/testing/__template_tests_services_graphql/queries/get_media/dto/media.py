from core.web.services.core.json import JsonObject


class DtoTitle(JsonObject):
    romaji: str = None
    english: str = None
    native: str = None


class DtoMedia(JsonObject):
    id: int = None
    title: DtoTitle = None

