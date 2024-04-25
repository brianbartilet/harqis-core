from core.web.browser.fixtures.base_page import BaseFixturePageObject


class BasePageHeroku(BaseFixturePageObject):
    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)

