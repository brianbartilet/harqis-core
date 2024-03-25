from dataclasses import dataclass
from typing import Optional, TypeVar, Union


@dataclass
class AppConfigWSClient:
    """
    Base configuration object for web services
    """
    client: str                      # type of service to be used: rest, curl, grpc, graphql
    parameters: {                    # keyword arguments to pass to required args: base_url
        "base_url": str,
        "response_encoding": Optional[str],
        "verify": Optional[bool],
        "timeout": Optional[int],
        "stream": [bool],
        "logging": Optional[str]


    }
    headers: Optional[dict] = None   # default headers to initialize the requests *USE CAREFULLY FOR AUTHORIZATION*
    app_data: Optional[dict] = None  # placeholder dictionary to contain other app context information e.g. api keys


T = TypeVar("T", bound=AppConfigWSClient)
TWSConfig = Union[T, dict]
