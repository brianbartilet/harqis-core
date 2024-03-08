from enum import Enum


class ServiceClientType(Enum):
    """
    Enum for different types of service clients.
    """
    WEBSERVICE_GENERIC = 'client'   # Generic web service client
    CURL = 'curl'                   # cURL client
    SOAP = 'soap'                   # SOAP client
    REST = 'rest'                   # REST client
    GRAPHQL = 'graphql'             # GraphQL client
    GRPC = 'grpc'                   # gRPC client
