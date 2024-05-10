from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from core.config.app_config import BaseAppConfigModel


@dataclass
class AppConfigWebDriver(BaseAppConfigModel):
    """
    Base configuration object for a web driver. This class extends the BaseAppConfigModel to provide
    specific configuration settings necessary for web drivers.

    Attributes:
        type (Optional[str]): Type of web driver to be used, such as Selenium or Playwright.
        browser (Optional[str]): Type of browser to be used.
        parameters (Dict[str, Any]): Contains default arguments to pass to the web driver, including:
            'url' (str): URL to be navigated to.
            'headless' (bool): Whether to run the browser in headless mode.
            'timeout' (int): Timeout for the web driver.
        options (Optional[str]): Additional optional settings for the web driver. Note that some options
            may not be available for all web drivers.
        headers (Optional[Dict[str, str]]): Default headers for initializing the web driver requests.
    """
    type: Optional[str] = None
    browser: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=lambda: {
        'url': '',                # Example default URL, adjust as necessary
        'headless': False,        # Default to not headless
        'timeout': 30             # Default timeout in seconds
    })
    options: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
