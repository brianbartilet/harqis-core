from behave import *

from demo.testing.example_features_webdriver.references.pages.status_codes import BasePageHerokuStatusCode


@given("I am on the {page_name} page")
def step_given_i_am_on_the_page(context, page_name):
    """
    This function is a step in the behave test that navigates to a specified page.
    Args:
        context (behave.runner.Context): The behave context.
        page_name (str): The name of the page to navigate to.
    """

    def get_page_status_codes():
        """
        This function returns an instance of the BasePageHerokuStatusCode class.
        """
        return BasePageHerokuStatusCode(context.driver)

    pages_map = {
        'status': get_page_status_codes
    }

    uri = pages_map[page_name]().uri
    context.driver.get(context.base_url + uri)