from core.web.browser.fixtures.base_page import *


class BasePageHeroku(BaseFixturePageObject):
    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)

