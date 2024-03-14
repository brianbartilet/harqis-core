from enum import Enum


class MimeType(Enum):
    """
    Enumeration of common MIME types for file formats.
    """
    APP_GZIP = "application/gzip"
    APP_JSON = "application/json"
    APP_PDF = "application/pdf"
    APP_XML = "application/xml"
    APP_ZIP = "application/zip"
    IMG_BMP = "image/bmp"
    IMG_GIF = "image/gif"
    IMG_JPEG = "image/jpeg"
    IMG_PNG = "image/png"
    TEXT_CSV = "text/csv"
    TEXT_HTML = "text/html"
    TEXT_PLAIN = "text/plain"
