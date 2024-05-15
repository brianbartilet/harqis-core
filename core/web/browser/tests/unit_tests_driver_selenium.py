import unittest
import os

from core.config.constants.environment import Environment
from core.config.env_variables import ENV

from core.web.browser.fixtures.web_driver import BaseFixtureWebDriverLoader
from core.web.browser.fixtures.base_page import BaseFixturePageObject
from core.web.browser.core.config.web_driver import AppConfigWebDriver

from selenium.webdriver.remote.webdriver import WebDriver

from core.config.loader import ConfigLoaderService


class TestWebDriverSelenium(unittest.TestCase):
    def setUp(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        load_config = ConfigLoaderService(file_name='config.yaml', base_path=base_path).config

        self.config_chrome = AppConfigWebDriver(**load_config['driver_selenium_chrome'])
        self.config_firefox = AppConfigWebDriver(**load_config['driver_selenium_firefox'])
        self.config_edge = AppConfigWebDriver(**load_config['driver_selenium_edge'])

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_create_webdriver_chrome(self):
        chrome = BaseFixtureWebDriverLoader(self.config_chrome)
        self.assertIsInstance(chrome.driver._driver, WebDriver)
        chrome.driver.quit()

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_create_webdriver_firefox(self):
        firefox = BaseFixtureWebDriverLoader(self.config_firefox)
        self.assertIsInstance(firefox.driver._driver, WebDriver)
        firefox.driver.quit()

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_create_webdriver_edge(self):
        edge = BaseFixtureWebDriverLoader(self.config_edge)
        self.assertIsInstance(edge.driver._driver, WebDriver)
        edge.driver.quit()

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_basic_webdriver_flow(self):
        chrome_driver = BaseFixtureWebDriverLoader(self.config_chrome)
        page = BaseFixturePageObject(**chrome_driver.properties)
        page.navigate_to_page()

        test_element = page.driver.find_element('id', 'content')
        self.assertIsNotNone(test_element)



