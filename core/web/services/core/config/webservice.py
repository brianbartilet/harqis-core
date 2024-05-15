from dataclasses import dataclass, field
from typing import Optional, Dict

from core.config.app_config import BaseAppConfigModel


@dataclass
class AppConfigWSClient(BaseAppConfigModel):
    """
    Base configuration object for web services.

    Attributes:
        client (str): Specifies the type of service to be used (e.g., REST, cURL, gRPC, GraphQL).
        parameters (Dict[str, Optional[any]]): Keyword arguments to pass to service, including
            base_url, response_encoding, verify, timeout, stream, and logging.
        headers (Optional[Dict[str, str]]): Default headers to initialize the requests. Use carefully,
            especially for authorization.
    """
    client: Optional[str] = None
    parameters: Dict[str, Optional[any]] = field(default_factory=lambda: {
        "base_url": None,
        "response_encoding": None,
        "verify": None,
        "timeout": None,
        "stream": False,
        "logging": None
    })
    headers: Optional[Dict[str, str]] = None
