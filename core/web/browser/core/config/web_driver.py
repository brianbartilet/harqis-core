from dataclasses import dataclass
from typing import Optional


@dataclass
class AppConfigWebDriver:
    """
    Base configuration object for a web driver
    """
    type: str                        # type of web driver to be used, selenium or playwright
    browser: str                     # type of browser to be used
    parameters: {                    # keyword arguments to pass to the web driver
        'url': str,                  # url to be navigated to
        'headless': bool             # whether to run the browser in headless mode
    }
    app_data: Optional[dict] = None  # placeholder dictionary to contain other app context information e.g. api keys
