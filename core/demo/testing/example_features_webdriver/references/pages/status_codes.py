from demo.testing.example_features_webdriver.references.base_page import BasePageHeroku
from selenium.webdriver.common.by import By


class BasePageHerokuStatusCode(BasePageHeroku):
    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.uri = '/status_codes'

    def get_link_status(self, status_code):
        return self.driver.find_element(By.XPATH, '//a[text()={status_code}]'
                                        .format(status_code=status_code))

    def get_link_status_text(self, status_code):
        xpath = '//p[contains(text(), "This page returned a {status_code} status code")]'.format(status_code=status_code)
        return self.driver.find_element(By.XPATH, xpath)

    def click_link_status(self, status_code):
        self.get_link_status(status_code).click()

    def did_page_load(self, status_code) -> bool:
        return self.get_link_status_text(status_code).is_displayed()


