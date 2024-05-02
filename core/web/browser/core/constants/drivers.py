from enum import Enum


class WebDriverNames(Enum):
    """
    Enum representing the names of various web drivers supported.

    Attributes:
        SELENIUM (str): Represents the Selenium WebDriver.
        PLAYWRIGHT (str): Represents the Playwright tool for browser automation.
    """
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"
    BEAUTIFULSOUP = "beautifulsoup"
