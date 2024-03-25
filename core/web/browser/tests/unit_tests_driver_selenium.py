import unittest

from core.web.browser.fixtures.web_driver import BaseFixtureWebDriver
from core.web.browser.core.config.web_driver import AppConfigWebDriver

from selenium.webdriver.remote.webdriver import WebDriver

from core.config.loader import ConfigFileLoader


class TestWebDriverSelenium(unittest.TestCase):
    def setUp(self):
        load_config = ConfigFileLoader(file_name='config.yaml').config

        self.config_chrome = AppConfigWebDriver(**load_config['driver_selenium_chrome'])
        self.config_firefox = AppConfigWebDriver(**load_config['driver_selenium_firefox'])
        self.config_edge = AppConfigWebDriver(**load_config['driver_selenium_edge'])

    def test_create_webdriver_chrome(self):
        chrome = BaseFixtureWebDriver(self.config_chrome)
        self.assertIsInstance(chrome.driver, WebDriver)
        chrome.driver.quit()

    def test_create_webdriver_firefox(self):
        firefox = BaseFixtureWebDriver(self.config_firefox)
        self.assertIsInstance(firefox.driver, WebDriver)
        firefox.driver.quit()

    def test_create_webdriver_edge(self):
        edge = BaseFixtureWebDriver(self.config_edge)
        self.assertIsInstance(edge.driver, WebDriver)
        edge.driver.quit()

    def test_basic_webdriver_flow(self):
        ...
