from core.testing.gherkin.behave.contracts.hooks import IBehaveHooks, log
from demo.testing.example_features_webdriver.config import CONFIG
from core.web.browser.fixtures.web_driver import BaseFixtureWebDriverLoader


class HooksWebDriver(IBehaveHooks):
    """
    This class implements the IBehaveHooks interface for the WebDriver.
    It defines hooks that are specific to the WebDriver, such as setting up and tearing down the WebDriver.
    """

    @staticmethod
    def before_all(context):
        """
        This hook is called before all tests are executed.
        It starts the WebDriver and stores it in the context for other steps to use.
        """
        log.info("Starting the browser..")
        context.driver = BaseFixtureWebDriverLoader(CONFIG).driver
        context.base_url = CONFIG.parameters['url']

    @staticmethod
    def before_scenario(context, scenario):
        """
        This hook is called before each scenario is tested.
        It navigates to the base URL specified in the configuration.
        """
        context.driver.get(CONFIG.parameters['url'])

    @staticmethod
    def after_scenario(context, scenario):
        ...

    @staticmethod
    def after_all(context):
        """
        This hook is called after all tests were executed.
        It quits the WebDriver, effectively closing the browser.
        """
        context.driver.quit()


