import requests

from typing import Type, TypeVar

from core.web.services.core.clients.base import BaseWebClient
from core.web.services.core.contracts.response import IResponse
from core.web.services.core.response import Response

TResponse = TypeVar('TResponse')
TErrors = TypeVar('TErrors')


class GraphQLClient(BaseWebClient):
    """
    A base class for a GraphQL web client that implements the IWebClient interface.
    This class provides common functionality for sending HTTP requests and processing responses.
    """
    def get_response(self, response: requests.Response, response_hook: Type[TResponse]) -> IResponse[TResponse]:
        """
        Processes the HTTP response and returns an IResponse instance.

        Args:
            response: The HTTP response received from the request.
            response_hook: The type to deserialize the response data into.

        Return:
            An instance of IResponse containing the processed response data.
        """
        self.response = Response(response_hook, data=None, response_encoding=self.response_encoding, data_key='data')
        self.response.set_status_code(response.status_code)
        self.response.set_headers(response.headers)
        self.response.set_raw_data(response.content)

        return self.response

    def get_errors(self) -> Response[TErrors]:
        error_response = Response(dict, data=None, response_encoding=self.response_encoding, data_key='errors')
        error_response.set_raw_data(self.response.raw_data)

        return error_response
