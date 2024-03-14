import os

from web.services.core.request_builder.base import RequestBuilder
from web.services.core.json import JsonObject
from web.services.core.constants.payload_type import PayloadType
from web.services.core.constants.http_headers import HttpHeaders
from web.services.core.constants.mime_type import MimeType
from web.services.core.constants.http_methods import HttpMethod

from utilities.resources.loader import ResourceDataLoader, Resource

from typing import Type, TypeVar

T = TypeVar('T')


class RequestBuilderGraphQL(RequestBuilder):
    """
    A builder class for constructing web service requests.
    """
    def __init__(self, gql_file: str, **kwargs):
        super(RequestBuilderGraphQL, self).__init__(**kwargs)
        self.gql_file = gql_file
        self.base_path = kwargs.get('base_path', os.getcwd())

        self\
            .set_method(HttpMethod.POST)\
            .add_header(HttpHeaders.CONTENT_TYPE, MimeType.APP_JSON.value)

    def set_variables(self, variables: Type[T]):
        if isinstance(variables, JsonObject):
            variables = variables.get_dict()
        else:
            variables = variables

        loader = ResourceDataLoader(Resource.GQL, self.gql_file, self.base_path, variables=variables)

        self.add_payload(loader.data, PayloadType.JSON)

        return self
