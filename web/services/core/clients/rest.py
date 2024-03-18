from typing import Type

from web.services.core.clients.base import BaseWebClient
from web.services.core.contracts.client import TClient


class RestClient(BaseWebClient):
    """
    A base class for a REST web client that implements the IWebClient interface.
    This class provides common functionality for sending HTTP requests and processing responses.
    """
