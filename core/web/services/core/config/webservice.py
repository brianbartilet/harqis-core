from dataclasses import dataclass
from typing import Optional

from core.config.app_config import BaseAppConfigModel


@dataclass
class AppConfigWSClient(BaseAppConfigModel):
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

