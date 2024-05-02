from demo.testing.example_features_webdriver.references.base_page import BasePageHeroku
from core.web.browser.fixtures.base_page import WebElement, List

from selenium.webdriver.common.by import By


class BasePageHerokuStatusCode(BasePageHeroku):
    def __init__(self, driver, **kwargs):
        """
        Initializes a new instance of the BasePageHerokuStatusCode class, which provides methods to interact
        with the status codes page.

        Args:
            driver: The WebDriver instance used to interact with the web page.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(driver, **kwargs)
        self.uri = '/status_codes'

    @property
    def status_code_links(self) -> List[WebElement]:
        """
        Returns a list of web elements representing the links to different status codes on the page.

        Returns:
            List[WebElement]: A list of WebElement instances representing the status code links.
        """
        elements = self.driver.find_elements(By.XPATH, '//a')
        return elements

    @property
    def status_code_success(self) -> WebElement:
        """
        Returns the WebElement corresponding to the '200' status code link.

        Returns:
            WebElement: The WebElement for the '200' status code link.
        """
        return self.driver.find_element(By.XPATH, '//a[text()="200"]')

    def get_link_status(self, status_code) -> WebElement:
        """
        Retrieves the link WebElement for a given status code.

        Args:
            status_code: The HTTP status code for which the link is needed.

        Returns:
            WebElement: The WebElement for the specified status code link.
        """
        return self.driver.find_element(By.XPATH, f'//a[text()="{status_code}"]')

    def get_link_status_text(self, status_code) -> WebElement:
        """
        Retrieves the WebElement containing the description text for a given status code.

        Args:
            status_code: The HTTP status code for which the description is needed.

        Returns:
            WebElement: The WebElement containing the description text.
        """
        xpath = f'//p[contains(text(), "This page returned a {status_code} status code")]'
        return self.driver.find_element(By.XPATH, xpath)

    def click_link_status(self, status_code) -> None:
        """
        Clicks on the link corresponding to a given status code.

        Args:
            status_code: The HTTP status code link to be clicked.
        """
        self.get_link_status(status_code).click()

    def did_page_load(self, status_code) -> bool:
        """
        Checks if the page associated with a given status code has loaded by verifying the display of the status code description.

        Args:
            status_code: The HTTP status code to check the page for.

        Returns:
            bool: True if the description text is displayed, otherwise False.
        """
        return self.get_link_status_text(status_code).is_displayed()
