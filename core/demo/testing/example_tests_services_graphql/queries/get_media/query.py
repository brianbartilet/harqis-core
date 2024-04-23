import os
from core.web.services.fixtures.graphql import BaseFixtureServiceGraphQL

from demo.testing.example_tests_services_graphql.queries.get_media.models.media import Media


class ServiceQueryGetMedia(BaseFixtureServiceGraphQL):
    """
    Service class for executing GraphQL queries related to media information.

    This class extends BaseFixtureServiceGraphQL to utilize pre-configured GraphQL queries
    for retrieving media data, facilitating the execution of these queries with variable inputs
    and handling their responses.

    Args:
        config: Configuration object providing necessary setup details for GraphQL services.
        gql_file (str): The name of the GraphQL file template used for queries. Defaults to 'get_media.tpl.gql'.
        **kwargs: Arbitrary keyword arguments that are passed to the superclass constructor.

    Attributes:
        path (str): The file system path of the directory containing this script, used to locate GraphQL templates.
    """
    def __init__(self, config, gql_file='get_media.tpl.gql', **kwargs):
        """
        Initializes the ServiceQueryGetMedia service with necessary configuration.

        Args:
            config: Configuration object passed to the BaseFixtureServiceGraphQL constructor.
            gql_file (str): GraphQL template file name. Defaults to 'get_media.tpl.gql'.
            **kwargs: Arbitrary keyword arguments passed along to the superclass.
        """
        self.path = os.path.dirname(os.path.abspath(__file__))
        super(ServiceQueryGetMedia, self)\
            .__init__(config, gql_file=gql_file, base_path=self.path, **kwargs)

    def get_query_media_with_test_case_data(self, sample_variables: dict):
        """
        Executes a GraphQL query to retrieve media information based on provided test case variables.

        Args:
            sample_variables (dict): A dictionary containing variables for the GraphQL query.

        Returns:
            The response from executing the GraphQL query with the specified variables.
        """
        self.request.set_variables(sample_variables)
        return self.client.execute_request(self.request.build())

    def get_query_media_with_test_response_hook(self, sample_variables: dict):
        """
        Executes a GraphQL query to retrieve media information and uses a response hook to process the response.

        The response hook is an instance of the Media class, which may be used to modify or validate the response data.

        Args:
            sample_variables (dict): A dictionary containing variables for the GraphQL query.

        Returns:
            The processed response from the GraphQL query, potentially altered or validated by the Media response hook.
        """
        self.request.set_variables(sample_variables)
        return self.client.execute_request(self.request.build(), response_hook=Media)



