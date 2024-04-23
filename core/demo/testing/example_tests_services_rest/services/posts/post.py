from core.web.services.core.constants.http_methods import HttpMethod

from demo.testing.example_tests_services_rest.services.base_service import BaseServiceApp
from demo.testing.example_tests_services_rest.models.user import User
from demo.testing.example_tests_services_rest.models.payload import PostPayload
from web.services.core.contracts.response import IResponse


class ServiceRestExamplePost(BaseServiceApp):
    """
     A class derived from BaseServiceApp to handle RESTful operations specifically for posts.
     This represents a URI resource along with all the http methods that can be performed on it.
     """

    def __init__(self, config, **kwargs):
        """
         Initializes the ServiceRestExamplePost with the necessary configuration and sets the URI parameter to 'posts'.
         Other specific headers or setup for the resource can be defined here

         Args:
             config: Configuration settings for the service application.
             **kwargs: Arbitrary keyword arguments that are passed to the parent class initializer.
         """
        resource = 'posts'
        super(ServiceRestExamplePost, self).__init__(config, **kwargs)
        self.request.add_uri_parameter(resource)

    def request_get(self):
        """
        Performs a GET request for a specific post using the URI parameter '1'.

        Returns:
            Response: The response object from the server after executing the POST request.
        """
        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter('1')

        return self.client.execute_request(self.request.build())

    def request_get_with_hook(self) -> IResponse[User]:
        """
        Performs a GET request for a specific post identified by the URI parameter '1'. This method sets up
        the request to retrieve a post, executes it, and processes the response through a specified hook to
        parse the server's response into an instance of the User model.

        Returns:
            IResponse[User]: The response object from the server, which includes the parsed data of the User model.
                             The response is processed by the 'response_hook' to convert JSON data into a User instance.
        """
        self.request \
            .set_method(HttpMethod.GET) \
            .add_uri_parameter('1')

        return self.client.execute_request(self.request.build(), response_hook=User)

    def request_post(self, payload: PostPayload):
        """
        Performs a POST request to create a new post with the given payload.

        Args:
            payload (PostPayload): The data to be sent in the request body.

        Returns:
            Response: The response object from the server after executing the POST request.
        """
        self.request \
            .set_method(HttpMethod.POST) \
            .add_json_body(payload)

        return self.client.execute_request(self.request.build())

    def request_delete(self):
        """
        Prepares a DELETE request to remove a specific post. This method does not execute the request but builds it for later execution.

        Returns:
            Request: The prepared DELETE request.
        """
        self.request \
            .set_method(HttpMethod.DELETE)

        return self.client.execute_request(self.request.build())
