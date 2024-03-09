from enum import Enum

class WSClientName(Enum):
    """
    Enum for different types of service clients.
    """
    GENERIC = 'web'     # Generic web service client
    CURL = 'curl'       # cURL client
    SOAP = 'soap'       # SOAP client
    REST = 'rest'       # REST client
    GRAPHQL = 'graphql' # GraphQL client
    GRPC = 'grpc'       # gRPC client

    def __str__(self):
        return self.value
