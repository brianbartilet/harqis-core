from enum import Enum


class ServiceClientType(Enum):
    WEBSERVICE = 'client'
    CURL = 'curl'
    WEBDRIVER = 'webdriver'
    SOAP = 'soap'
    REST = 'rest'
