import unittest
from web.base.apps.browser.webdriver_factory import *


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