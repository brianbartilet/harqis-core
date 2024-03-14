from dataclasses import dataclass
from typing import Optional


@dataclass
class AppConfigWSClient:
    """
    Base configuration object for web services
    """
    app_id: str                     # unique identifier for application configuration
    client: str                     # type of service to be used: rest, curl, grpc, graphql
    parameters: dict                # keyword arguments to pass to required args: base_url
    headers: Optional[dict] = None  # default headers to initialize the requests *USE CAREFULLY FOR AUTHORIZATION*
    app_data: Optional[dict] = None # placeholder dictionary to contain other app context information e.g. api keys
