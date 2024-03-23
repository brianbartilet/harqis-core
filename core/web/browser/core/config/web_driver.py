from dataclasses import dataclass
from typing import Optional


@dataclass
class AppConfigWebDriver:
    """
    Base configuration object for web services
    """
    type: str                        # type of web driver to be used, selenium or playwright
    browser: str                     # type of browser to be used
    parameters: dict                 # keyword arguments to pass to the web driver
    app_data: Optional[dict] = None  # placeholder dictionary to contain other app context information e.g. api keys
