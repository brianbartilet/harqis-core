from enum import Enum


class PayloadType(Enum):
    FILE = 'files'
    JSON = 'json'
    XML = 'xml'
    DICT = 'data'
    UNKNOWN = 'data'
    TEXT = 'data'
