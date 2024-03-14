import requests

from typing import Type, TypeVar

from web.services.core.clients.base import BaseWebClient
from web.services.core.contracts.response import IResponse
from web.services.core.response import Response

T = TypeVar('T')


class GraphQLClient(BaseWebClient):
    """
    A base class for a GraphQL web client that implements the IWebClient interface.
    This class provides common functionality for sending HTTP requests and processing responses.
    """
    def get_response(self, response: requests.Response, response_hook: Type[T]) -> IResponse[T]:
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

    def get_errors(self) -> Response[T]:
        error_response = Response(dict, data=None, response_encoding=self.response_encoding, data_key='errors')
        error_response.set_raw_data(self.response.raw_data)

        return error_response
