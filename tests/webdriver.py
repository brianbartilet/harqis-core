import unittest
from web.base.webdriver_factory import *
from selenium.common.exceptions import WebDriverException


class TestWebdriver(unittest.TestCase):

    def test_webdriver_context(self):

        kwargs = {
            'browser': 'chrome',
            'args': [
                "start-maximized",
                "disable-extensions",
                "no-default-browser-check",
                "--window-size=1920,1020"
            ],

        }

        with WebDriverFactory.create_webdriver(**kwargs) as driver:

            driver.get('https://facebook.com')

            raise Exception