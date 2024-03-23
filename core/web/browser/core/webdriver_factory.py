"""
WebDriver Factory class implementation
It creates a web driver instance based on browser configurations
Example:
    wdf = WebDriverFactory(browser)
    wdf.get_web_driver_instance()
"""
import sys

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

#from win32api import GetFileVersionInfo, LOWORD, HIWORD

from contextlib import contextmanager


class WebDriverFactory:

    def __init__(self):
        """
        Inits WebDriverFactory class

            Currently runs on windows

        Returns:
            None
        """

    @contextmanager
    def create_webdriver(*args, **kwargs) -> WebDriver:
        driver = WebDriverFactory.get_web_driver_instance(*args, **kwargs)
        try:
            yield driver

        except Exception as e:
            prefix = re.sub('[^a-zA-Z0-9\n\.]', '', driver.title)
            file_name = '{0}_{1}_{2}.png'.format(type(e).__name__, prefix, datetime.now().strftime('%Y%m%d%H%M'))
            err_scr = kwargs.get("enable_screenshot_on_error", True)
            if err_scr:
                scr_path = os.path.join(os.getcwd(), "screenshots")
                if not os.path.exists(scr_path):
                    os.makedirs(scr_path)
                file = kwargs.get(os.path.join("screenshot_path", file_name),
                                  os.path.join(scr_path, file_name)
                                  )
                try:
                    driver.save_screenshot(file)
                finally:
                    print("Failed to take screenshot on error.")
        finally:
            driver.close()

    @staticmethod
    def get_web_driver_instance(browser, maximize_start=True, **kwargs) -> WebDriver:
        """
        SAMPLE CONFIG:
        webdriver:
            browser: 'headless'
            args:
              - "start-maximized"
              - "disable-extensions"
              - "no-default-browser-check"
              - "--window-size=1920,1020"
              - "user-data-dir={USER_DIRECTORY}"
              - "--proxy-server={HTTP_URL}"
        """

        download_folder = kwargs.get('download_folder')
        # or set any folder to PATH environment variable
        base_driver_path = kwargs.get('base_driver_path', os.path.join(ENV_ROOT_DIRECTORY, "Core\web\drivers"))
        target_driver_version = kwargs.get('target_driver_version')
        driver_args = kwargs.get('args', [])

        if browser == "chrome" or browser == "headless":
            chrome_options = webdriver.ChromeOptions()
            for args in driver_args:
                chrome_options.add_argument(args)
            if browser == "headless":
                chrome_options.add_argument("--headless")

            if download_folder is not None:
                options = {
                    "profile.default_content_settings.popups": 0,
                    "download.default_directory": download_folder
                    }
                chrome_options.add_experimental_option("prefs", options)

            driver = WebDriverFactory\
                .__get_chrome_instance(chrome_options, base_driver_path, target_driver_version)

            if maximize_start:
                driver.maximize_window()

            return driver

        elif browser == "firefox":
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument("start-maximized")
            driver = webdriver.Firefox()

            return driver

        raise Exception("The browser {} is not a valid option.".format(browser))

    @staticmethod
    def __get_chrome_instance(chrome_options, chrome_browser_path=None, chrome_version=None):

        if chrome_version is not None:
            version = '_{0}'.format(chrome_version) if chrome_version is not None else ''
            exe_path = r'{0}'.format(os.path.join(chrome_browser_path, 'chromedriver' + version + '.exe'))

            server_chrome_version = str(WebDriverFactory.__get_version_number(exe_path)[0])
            if server_chrome_version == chrome_version:
                try:
                    return webdriver.Chrome(chrome_options=chrome_options, executable_path=exe_path)
                except Exception as ex:
                    raise Exception("Chrome driver version does not exist: " + server_chrome_version)
            else:
                raise Exception("Chrome browser version installed is : " + server_chrome_version
                                + " but expected is :" + chrome_version)
        else:
            return webdriver.Chrome(chrome_options=chrome_options)

    @staticmethod
    def __get_version_number(filename):
        try:
            if sys.platform == 'win32':
                info = GetFileVersionInfo(filename, "\\")
                ms = info['FileVersionMS']
                ls = info['FileVersionLS']
                version = HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls)
            else:
                raise NotImplementedError

            return version
        except Exception as ex:
            raise Exception("Get Chrome version error: " + ex.args[2])
