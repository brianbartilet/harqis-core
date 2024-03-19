from enum import Enum


class HttpHeaders(Enum):
    """
    Enum for common HTTP header names.
    """
    ACCEPT = 'Accept'
    ACCEPT_CHARSET = 'Accept-Charset'
    AUTHORIZATION = 'Authorization'
    CONTENT_TYPE = 'Content-Type'
    ORIGIN = 'Origin'
    USER_AGENT = 'User-Agent'
    CACHE_CONTROL = 'Cache-Control'
    CONNECTION = 'Connection'
    ACCEPT_ENCODING = 'Accept-Encoding'
    HOST = 'Host'
    REFERER = 'Referer'
    X_REQUESTED_WITH = 'X-Requested-With'
    COOKIE = 'Cookie'
    CONTENT_LENGTH = 'Content-Length'
    ETAG = 'ETag'
    IF_NONE_MATCH = 'If-None-Match'
    SET_COOKIE = 'Set-Cookie'
