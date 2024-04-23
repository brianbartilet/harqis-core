from enum import Enum


class MediaStatus(Enum):
    """
    Defines the various statuses that media items can possess within an application.

    Attributes:
        REPEATING (str): Represents a status where the media item is set to repeat continuously.
    """
    REPEATING = 'REPEATING'
