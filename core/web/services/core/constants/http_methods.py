from enum import Enum


class HttpMethod(Enum):
    """
    Enum for common HTTP methods.
    """
    COPY = 'copy'
    DELETE = 'delete'
    GET = 'get'
    HEAD = 'head'
    MERGE = 'merge'
    OPTIONS = 'options'
    PATCH = 'patch'
    POST = 'post'
    PUT = 'put'

    def __str__(self):
        return self.value