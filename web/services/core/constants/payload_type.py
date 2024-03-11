from enum import Enum


class PayloadType(Enum):
    """
    Enum for different types of payloads in HTTP requests.
    """
    FILE = 'files'   # For multipart-encoded files.
    JSON = 'json'    # For JSON payload.
    XML = 'xml'      # For XML payload.
    DICT = 'data'    # For form-encoded data.
    UNKNOWN = 'data' # Fallback for unknown payload types.
    TEXT = 'data'    # For plain text payload.

    