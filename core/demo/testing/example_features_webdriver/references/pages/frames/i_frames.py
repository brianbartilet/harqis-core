from demo.testing.example_features_webdriver.references.base_page import BasePageHeroku


class BasePageHerokuIFrames(BasePageHeroku):
    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
