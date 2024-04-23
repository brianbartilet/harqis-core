from core.web.services.core.json import JsonObject


class Title(JsonObject):
    """
    Represents different linguistic versions of a title for media content.

    Attributes:
        romaji (str): The title of the media in Romaji (Latin script used in Japanese context).
        english (str): The title of the media in English.
        native (str): The native script title of the media (e.g., Japanese characters).
    """
    romaji: str = None
    english: str = None
    native: str = None


class Media(JsonObject):
    """
    Represents a media item, encapsulating various properties including its title.

    Attributes:
        id (int): The unique identifier for the media.
        title (Title): An instance of the Title class that stores the media title in various languages.
    """
    id: int = None
    title: Title = None

