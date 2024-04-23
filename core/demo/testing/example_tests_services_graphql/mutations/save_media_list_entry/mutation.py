import os
from core.web.services.fixtures.graphql import BaseFixtureServiceGraphQL


class ServiceMutationSaveMediaListEntry(BaseFixtureServiceGraphQL):
    """
    A service class for handling mutations to save media list entries using GraphQL.

    Extends the BaseFixtureServiceGraphQL to utilize its GraphQL execution capabilities,
    particularly for handling operations related to media list entries.

    Attributes:
        path (str): The directory path of the current file, used for locating GraphQL templates.

    Args:
        config: Configuration object containing settings for GraphQL service operations.
        gql_file (str): The name of the GraphQL file template used for the mutation.
            Defaults to 'save_media_list_entry.tpl.gql'.
        **kwargs: Additional keyword arguments that are passed to the parent class constructor.
    """
    def __init__(self, config, gql_file: str = 'save_media_list_entry.tpl.gql', **kwargs):
        """
        Initializes the ServiceMutationSaveMediaListEntry service with necessary configuration.

        Args:
            config: Passed to the BaseFixtureServiceGraphQL constructor.
            gql_file (str): The GraphQL template file name.
                Defaults to 'save_media_list_entry.tpl.gql' from the current directory.
            **kwargs: Arbitrary keyword arguments passed along to the superclass.
        """
        self.path = os.path.dirname(os.path.abspath(__file__))
        super(ServiceMutationSaveMediaListEntry, self)\
            .__init__(config, gql_file=gql_file, base_path=self.path, **kwargs)

    def test_mutation_save_media_with_test_case_data(self, sample_variables: dict):
        """
        Executes a GraphQL mutation to save a media list entry using provided test case data.

        Args:
            sample_variables (dict): A dictionary containing variables for the GraphQL mutation,
                                     typically including data like media item details.

        Returns:
            The result of the GraphQL mutation execution, typically including success status or data returned by the mutation.
        """
        self.request.set_variables(sample_variables)
        return self.client.execute_request(self.request.build())