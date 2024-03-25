from enum import Enum


class BrowserNames(Enum):
    """
    Enum defining browser names supported for web automation.

    Attributes:
        CHROME (str): Identifier for Google Chrome browser.
        FIREFOX (str): Identifier for Mozilla Firefox browser.
        EDGE (str): Identifier for Microsoft Edge browser.
    """
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
