from behave import *
from demo.testing.example_features_webdriver.references.pages.status_codes import BasePageHerokuStatusCode
from hamcrest import equal_to


@when("I select with type {status_code} status")
def when_i_select_with_type_status(context, status_code):
    """
    This function is a step in the behave test that selects a status code on the page.
    Args:
        context (behave.runner.Context): The behave context.
        status_code (str): The status code to select.
    """
    page_status = BasePageHerokuStatusCode(context.driver)
    context.status_code = status_code
    page_status.click_link_status(status_code)


@then("the page for the status is loaded successfully")
def when_i_select_with_type_status(context):
    """
    This function is a step in the behave test that verifies the page for the selected status code is loaded successfully.
    Args:
        context (behave.runner.Context): The behave context.
    """
    page_status = BasePageHerokuStatusCode(context.driver)
    check = page_status.did_page_load(context.status_code)
    page_status.verify.common.assert_that(check, equal_to(True), "The page did not load successfully")