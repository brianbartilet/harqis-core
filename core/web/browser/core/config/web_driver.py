from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AppConfigWebDriver:
    """
    Base configuration object for a web driver
    """
    type: str                                  # type of web driver to be used, selenium or playwright
    browser: str                               # type of browser to be used
    parameters: {                              # default arguments to pass to the web driver
        'url': str,                            # url to be navigated to
        'headless': bool,                      # whether to run the browser in headless mode
        'timeout': int,                        # timeout for the web driver
    }
    # **IMPORTANT** The following attributes are optional and should be set to None if not used as some options
    # may not be available for all web drivers
    options: Optional[str] = None              # additional options to pass to the web driver
    app_data: Optional[Dict[str, Any]] = None  # placeholder dictionary to contain other app information e.g. api keys
