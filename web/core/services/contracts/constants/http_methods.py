from enum import Enum


class Method(Enum):
    COPY = 'copy'
    DELETE = 'delete'
    GET = 'get'
    HEAD = 'head'
    MERGE = 'merge'
    OPTIONS = 'options'
    PATCH = 'patch'
    POST = "post"
    PUT = "put"
