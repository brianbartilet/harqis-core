from enum import Enum


class ServiceClientType(Enum):
    WEBSERVICE = 'client'
    CURL = 'curl'
    SOAP = 'soap'
    REST = 'rest'
