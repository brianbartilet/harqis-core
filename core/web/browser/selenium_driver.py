
import time
import os

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import *

from behave.runner import Context

from core.exception.error_wrapper import *
from core.utilities.logging.custom_logger import create_logger

future_speed = os.getenv("FUTURE_SPEED", "N").lower()


def find_element(locator: By, locator_value: str, suppress_errors=False):
    def decorator(func):
        def wrapper(*args):
            if suppress_errors:
                try:
                    return args[0].driver.find_element(locator, locator_value)
                except NoSuchElementException:
                    return None
            else:
                return args[0].driver.find_element(locator, locator_value)
        return wrapper
    return decorator


def find_elements(locator: By, locator_value: str):
    def decorator(func):
        def wrapper(*args) -> []:
            return args[0].driver.find_elements(locator, locator_value)
        return wrapper
    return decorator


class SeleniumDriver:

    log = create_logger()

    _type_map = {"id": By.ID,
                 "name": By.NAME,
                 "css": By.CSS_SELECTOR,
                 "xpath": By.XPATH,
                 "class": By.CLASS_NAME,
                 "link": By.LINK_TEXT,
                 "tag": By.TAG_NAME,
                 "partial_link_text": By.PARTIAL_LINK_TEXT
                 }

    #  provision for future update
    #  wait_time = os.getenv("SPEED", 1)

    locator_dictionary = {}

    def __init__(self, ctx, tmp_ctx=None, default_wait_time=2):
        """
        Added two context parameters for backward compatibility, to both process the old
        driver instance or the recent behave context.driver

        :param ctx: for new page objects or to update we can just pass the context
        to the page constructor

        :param tmp_ctx: for backwards compatibility, we can pass the context
        as an optional parameter to update methods or create new ones

        """

        if isinstance(ctx, Context):
            self.driver = ctx.driver
            self.context = ctx
            self.data = ctx.data
        elif isinstance(ctx, WebDriver):
            self.driver = ctx
            if tmp_ctx is not None:
                self.context = tmp_ctx
                self.data = tmp_ctx.app_data
        elif ctx is None:
            self.log.warning("Context detected as None. No browser instance created.")
        else:
            self.log.error("Failed to create webdriver instance.")

        self.default_wait_time = default_wait_time

        # since we've merged two waits, I believe it's logical to set the default time
        # to be twice the default
        self.jquery_wait_time = default_wait_time * 2
        self.get_element_buffer = float(os.getenv("SPEED", 0))

    def log_screen_shot(self):
        """
        Take screenshots from PO context

        """
        if not os.path.exists(self.context.env_output_path):
            os.makedirs(self.context.env_output_path)

        file_name = "{}{}{}".format(self.context.env_screen_shot_file_name[0:100], '_', time.time())

        path = os.path.join(self.context.env_output_path, file_name)[0:250] + '.png'
        self.context.driver.maximize_window()
        self.context.driver.save_screenshot(path)

    @handle_exception(NoSuchElementException, "Button Not Found")
    def click_on_button_with_text(self, button_text, base_element=None):
        """
        Click a button with a text
        :param button_text: Save, Back, Continue
        :param base_element: Pass the base element
        :return:
        """
        # this was added to allow descendant from anchor points
        xpath_base = ("./descendant::", "//")[base_element is None]
        x_path = "{}button[normalize-space(.)='{}']".format(xpath_base, button_text)
        self.scroll_to_element_and_click(x_path, "xpath", base_element)

    @handle_exception(NoSuchElementException, "Link Not Found")
    def click_on_link_with_text(self, link_text):
        """ single click an element where the link has the supplied text.
        :param link_text: text in the link name
        """
        self.element_click(link_text, locator_type="link")
        self._wait_for_jQuery()

    @handle_exception(NoSuchElementException, "Link Not Found Containing Text")
    def click_on_link_containing_text(self, link_text):
        """
        Click a link containing a text
        :param link_text:
        :return:
        """
        self.element_click(link_text, locator_type="partial_link_text")
        self._wait_for_jQuery()

    @handle_exception(NoSuchElementException, "Menu Not Found")
    def click_menu(self, locator, locator_type="id"):
        """
        Click a Menu name
        :param locator:
        :param locator_type:
        :return:
        """
        element = self.get_element(locator, locator_type)
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.click(element)
        action.perform()
        self.log.debug("Menu Item clicked with locator: {} and locatorType: {}".format(locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    def click_element_when_ready(self, locator, locator_type, timeout=15, poll_frequency=0.3):
        """
        Click an element when ready
        :param locator:
        :param locator_type:
        :param timeout:  Default timeout = 15
        :param poll_frequency: Default to poll value to 0.3
        :return:
        """
        # added where it checks that the element appears - other methods try to get the element
        if self.wait_for_element_to_appear(locator, locator_type, timeout, poll_frequency):
            self.scroll_to_element_and_click(locator, locator_type)

    @handle_exception(NoSuchElementException, "Element Not Found")
    def element_click(self, locator, locator_type="id", base_element=None):
        """
        Click a Selenium Web element
        :param locator:
        :param locator_type:
        :param base_element:
        :return:
        """
        if base_element is None:
            element = self.get_element(locator, locator_type)
        else:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = base_element.find_element(by_type, locator)
        if not self.is_element_visible_e(element):
            self.scroll_to_element_e(element)
        self.high_light_element(element)
        self.wait_for_element_to_be_clickable(element).click()
        # this replaces the jquery
        self._button_post_check_(element, 0.1)
        self.log.debug("Clicked on locator: {} and locatorType: {}".format(locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    def element_submit(self, locator, locator_type="id"):
        """
        Element submit
        :param locator:
        :param locator_type:
        :return:
        """
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        element.submit()
        self.log.debug("Submit on with locator: {} and locatorType: {}".format(locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    def element_get_text(self, locator, locator_type="id", base_element=None, strip_whitespaces=False):
        """
        Get text for a given Element
        :param locator:
        :param locator_type:
        :param base_element:
        :param strip_whitespaces: boolean value to strip whietspace
        :return:
        """
        if base_element is None:
            element = self.get_element(locator, locator_type)
        else:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = base_element.find_element(by_type, locator)
        self.high_light_element(element)

        if not self.is_element_visible_e(element):
            self.scroll_to_element_e(element)
        ele_text = element.text
        self.log.debug("Got the text {} on element with locator: {} and locatorType: {}".
                       format(ele_text.encode("utf-8"), locator, locator_type))

        if strip_whitespaces is True:
            ele_text.strip()

        return ele_text

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def element_get_value(self, locator, locator_type="id", base_element=None, strip_whitespaces=False):
        """
        Get the element attribute  value
        :param locator:
        :param locator_type:
        :param base_element:
        :param strip_whitespaces:
        :return: return the value
        """
        if base_element is None:
            element = self.get_element(locator, locator_type)
        else:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = base_element.find_element(by_type, locator)
        self.high_light_element(element)
        ele_text = element.get_attribute('value')
        self.log.debug("Got the attribute value {} on element with locator: {} and locatorType: {}".
                       format(ele_text, locator, locator_type))

        if strip_whitespaces is True:
            return ele_text.strip()

        return ele_text

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def element_get_title(self, locator, locator_type="id", base_element=None, strip_whitespaces=False):
        """
        Get Page Tile for a given element
        :param locator:
        :param locator_type:
        :param base_element:
        :param strip_whitespaces:
        :return:
        """
        if base_element is None:
            element = self.get_element(locator, locator_type)
        else:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = base_element.find_element(by_type, locator)

        self.high_light_element(element)
        ele_text = element.get_attribute('title')
        self.log.debug("Got the attribute title {} on element with locator: {} and locatorType: {}".
                       format(ele_text, locator, locator_type))

        if strip_whitespaces:
            return ele_text.strip()

        return ele_text

    @handle_exception(NoSuchElementException, "Element Not Found From Presence Check", ignore_exception=True)
    def element_presence_check(self, locator, by_type):
        """
        Check the element is presence on the screen
        :param locator:
        :param by_type:
        :return: return boolean value
        """
        element_list = self.driver.find_elements(by_type, locator)
        if len(element_list) > 0:
            return True
        else:
            return False

    @handle_exception(NoSuchElementException, "Element Input Text Not Found")
    @handle_exception(ElementNotVisibleException, "Element Input Text Not Visible")
    @handle_exception(ElementNotSelectableException, "Element Input Text Disabled")
    def enter_text_value(self, data, locator, locator_type="id", base_element=None):
        """
        Enter a text value for text field.
        :param data:
        :param locator:
        :param locator_type:
        :param base_element:
        :return:
        """
        if data is not None:
            if base_element is None:
                element = self.get_element(locator, locator_type)
            else:
                locator_type = locator_type.lower()
                by_type = self.get_by_type(locator_type)
                element = base_element.find_element(by_type, locator)
            self.high_light_element(element)
            element.clear()
            element.send_keys(data)
            element.send_keys(Keys.TAB)
            self.log.debug("Send keys {} on locator: {} and locatorType: {}".format(data, locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Input Text Not Found")
    @handle_exception(ElementNotVisibleException, "Element Input Text Not Visible")
    @handle_exception(ElementNotSelectableException, "Element Input Text Disabled")
    def enter_text_value_for_prepopulated_field(self, data, locator, locator_type="id", base_element=None):
        """
        Enter a text value for pre populated text field
        :param data:
        :param locator:
        :param locator_type:
        :param base_element:
        :return:
        """
        if data is not None:
            if base_element is None:
                element = self.get_element(locator, locator_type)
            else:
                locator_type = locator_type.lower()
                by_type = self.get_by_type(locator_type)
                element = base_element.find_element(by_type, locator)
            self.high_light_element(element)
            element.clear()
            element.send_keys((Keys.CONTROL, "a"))
            element.send_keys(data)
            element.send_keys(Keys.TAB)
            self.log.debug("Send keys {} on locator: {} and locatorType: {}".format(data, locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(ElementNotVisibleException, "Element Not Visible")
    @handle_exception(ElementNotSelectableException, "Element Disabled")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def is_element_enabled(self, locator, locator_type="id", base_element=None):
        """
        Check is the element is enabled
        :param locator:
        :param locator_type:
        :param base_element:
        :return:
        """
        if base_element is None:
            element = self.get_element(locator, locator_type)
        else:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = base_element.find_element(by_type, locator)
        if not self.is_element_visible_e(element):
            self.scroll_to_element_e(element)
            self._wait_for_jQuery()
            self.high_light_element(element)
            self.log.debug("Checking  on locator: {} and locatorType: {}".format(locator, locator_type))
        return self.verify_if_element_present_and_enabled(element)

    def is_element_present(self, locator, locator_type="id", timeout=None, highlight_element=True):
        """
        Check is the element present on the screen
        :param locator:
        :param locator_type:
        :param timeout:
        :param highlight_element:
        :return:
        """
        buffer = (0, self.get_element_buffer)[timeout is None]
        timeout = (timeout, self.default_wait_time)[timeout is None]
        timeout += buffer

        # replaced implementation as suggested by Madhu due
        # to the log.error in the previous implementation
        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        element = WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located((by_type, locator)))

        if highlight_element:
            self.high_light_element(element)
            return element is not None
        else:
            return False

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(ElementNotVisibleException, "Element Not Visible")
    @handle_exception(ElementNotSelectableException, "Element Disabled")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def is_element_selected(self, locator, locator_type="id"):
        """
        Check is the element is selected by locator
        :param locator:
        :param locator_type:
        :return:
        """
        element = self.get_element(locator, locator_type)
        return element.is_selected()

    @handle_exception(NoSuchElementException, "Element Not Found From Presence Check", ignore_exception=True)
    def is_element_selected_e(self, element):
        """
        Check is the element is selected by Element
        :param element:
        :return:
        """
        return element.is_selected()

    @handle_exception(NoSuchElementException, "Element Not Found From Presence Check", ignore_exception=True)
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def is_element_visible(self, locator, locator_type="id"):
        """
        Check is the element is visible on the screen by locator
        :param locator:
        :param locator_type:
        :return:
        """
        element = self.get_element(locator, locator_type)
        if WebDriverWait(self.driver, self.default_wait_time).until(
                ec.visibility_of(element)) is not None:
            return True

        return False

    def is_element_visible_e(self, element):
        """
        Check is the element is visible by element
        :param element:
        :return:
        """
        if WebDriverWait(self.driver, self.default_wait_time).until(
                ec.visibility_of(element)) is not None:
            return True

        return False

    @handle_exception(KeyError, "Locator Exception Encountered")
    @handle_exception(AttributeError, "Attribute Exception Encountered")
    def get_by_type(self, locator_type):
        """
        Get locator type
        :param locator_type:
        :return:
        """

        locator_type = locator_type.lower()
        result = self._type_map.get(locator_type)

        return result

    def get_element(self, locator_type="id", locator=""):
        """
        Get web element
        :param locator:
        :param locator_type:
        :return:
        """
        locator_type = locator_type.lower()
        element = self.driver.find_element(locator_type, locator)

        self.high_light_element(element)
        self.log.debug("Element found with locator: {} and locatorType: {}".format(locator, locator_type))

        return element

    @handle_exception(KeyError, "Locator Exception Encountered")
    @handle_exception(AttributeError, "Attribute Exception Encountered")
    def get_key_dic(self, locator):
        """
        Get the Key name by the locator value
        :param locator: locator can be id, name , xpath
        :return:
        """
        key = [key for key, value in self.locator_dictionary.items() if value[0] == locator][0]
        if len(key) > 0:
            return key
        else:
            return ""

    @handle_exception(KeyError, "Dictionary Key Error Encountered")
    @handle_exception(AttributeError, "Attribute Exception Encountered")
    def get_key_locator_type(self, locator):
        """
        Get the Key name by the locator value
        :param locator: locator can be id, name , xpath
        :return:
        """
        key = [key for key, value in self.locator_dictionary.items() if value[1] == locator][0]
        if len(key) > 0:
            return key
        else:
            return ""

    @handle_exception(NoSuchElementException, "Element Not Found")
    def get_element_e(self, base_element, locator, locator_type="id"):
        """
        Get element for a given base element
        :param base_element:
        :param locator:
        :param locator_type:
        :return:
        """
        if future_speed == "n":
            self._pause()
        # might remove the pause above
        else:
            self.wait_for_element_to_be_present(locator, locator_type, int(self.get_element_buffer))

        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        element = base_element.find_element(by_type, locator)
        self.high_light_element(element)
        self.log.debug("Element found with locator: {} and locatorType: {}".format(locator, locator_type))

        return element

    @handle_exception(NoSuchElementException, "Element Not Found")
    def get_elements(self, locator, locator_type="id"):
        """
        Get list of element for a given locator
        :param locator:
        :param locator_type:
        :return:
        """
        self.wait_for_multiple_elements_to_be_present(locator, locator_type, int(self.get_element_buffer))

        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        element_list = self.driver.find_elements(by_type, locator)
        if len(element_list) > 0:
            self.log.debug("Elements found with locator: {}".format(locator, locator_type))
            return element_list
        else:
            self.log.debug("Elements not found with locator: {}".format(locator, locator_type))
            return None

    @handle_exception(NoSuchElementException, "Element Not Found")
    def get_elements_by_tag_name(self, name):
        """
        Get list of elements by tag name
        :param name:
        :return:
        """
        return self.driver.find_elements_by_tag_name(name)

    @handle_exception(NoSuchElementException, "Element Not Found")
    def get_elements_e(self, base_element, locator, locator_type="id"):
        """
        Get list of elements for given base element
        :param base_element:
        :param locator:
        :param locator_type:
        :return:
        """

        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        element_list = base_element.find_elements(by_type, locator)
        if len(element_list) > 0:
            self.log.debug("Elements found with locator: {}".format(locator, locator_type))

            return element_list
        else:
            self.log.debug("Elements not found with locator: {}".format(locator, locator_type))

            return None

    @handle_exception(NoSuchElementException, "Element Not Found")
    def get_parent_l(self, locator, locator_type='id'):
        """
        Get parent element for a given locator
        :param locator:
        :param locator_type:
        :return:
        """
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        self.get_parent_e(element)
        self.log.debug("get_parent_l on locator: {} and locatorType: {}".format(locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    def get_parent_e(self, element):
        """
        Get parent element for given base element
        :param element:
        :return:
        """
        parent = self.driver.execute_script("return arguments[0].parentNode;", element)

        self.log.info("Parent Element found")
        return parent

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(AttributeError, "Attribute Exception Encountered")
    def high_light_element(self, element):
        """
        High light the element using a javascript
        :param element:
        :return:
        """

        # self.driver = element._parent
        def apply_style(s):
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                       element, s)
            self.log.warn("Potential issue with slow loading - executed script on previous screen.")

        original_style = element.get_attribute('style')
        apply_style("background: yellow; border: 2px solid red;")
        time.sleep(.2)
        apply_style(original_style)

    @handle_exception(NoSuchElementException, "Element Not Found")
    def move_to_element_and_click(self, locator, locator_type="id", base_element=None):
        """
        Move to the Element and click
        :param locator:
        :param locator_type:
        :param base_element:
        :return:
        """
        if base_element is None:
            element = self.get_element(locator, locator_type)
        else:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = base_element.find_element(by_type, locator)

        self.high_light_element(element)
        self.move_to_element_and_click_e(element)
        self.log.debug("Moved and clicked on locator: {} and locatorType: {}".format(locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    def move_to_element_and_click_e(self, element):
        """
        Move to element and click for given base element
        :param element:
        :return:
        """
        self.move_to_element_e(element)
        self.wait_for_element_to_be_clickable(element).click()
        self.log.debug("Moved and clicked element")

    @handle_exception(NoSuchElementException, "Element Not Found")
    def move_to_element_l(self, locator, locator_type="id"):
        """
        Move to the element for given locator
        :param locator:
        :param locator_type:
        :return:
        """
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        self.move_to_element_e(element)
        self.log.debug("Moved to element with locator: {} and locatorType: {}".format(locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(AttributeError, "Attribute Exception Encountered")
    def move_to_element_e(self, element):
        """
        Move to element for given base element
        :param element:
        :return:
        """
        ActionChains(self.driver) \
            .move_to_element(element) \
            .perform()
        self._wait_for_jQuery()
        self.log.debug("Moved to element")

    @handle_exception(NoSuchElementException, "Element Not Found")
    def navigate_to_page(self, navigation_path):
        """ Navigate to page using a navigation path.

        The navigation path is a series of links to click each separated with a '.'.
        e.g. Basic Details.Address Details will click on a link "Basic Details" and then on
        link "Address Details"

        :param navigation_path: '.' delimeted links to click on.
        """
        for navitem in navigation_path.split('.'):
            self.click_on_link_with_text(navitem)

    @handle_exception(WebDriverException, "WebDriver Error Encountered")
    def navigate_to_url(self, url):
        self.driver.get(url)

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(AttributeError, "Attribute Exception Encountered")
    def scroll_to_element_and_click(self, locator, locator_type="id", base_element=None):
        """
        Scroll to Element and Click the elements
        :param locator:
        :param locator_type:
        :param base_element: Pass the Base Element
        :return:
        """
        if base_element is None:
            element = self.get_element(locator, locator_type)
        else:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = base_element.find_element(by_type, locator)

        self.scroll_to_element_e(element)
        self.high_light_element(element)
        self.wait_for_element_to_be_clickable(element).click()

        # check one or the other
        self._button_post_check_(element, 0.1)
        self.log.debug("Moved and clicked on locator: {} and locatorType: {}".format(locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(AttributeError, "Attribute Exception Encountered")
    def scroll_to_element_l(self, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        self.scroll_to_element_e(element)
        self.log.debug("Scrolled to element with locator: {} and locatorType: {}".format(locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(AttributeError, "Attribute Exception Encountered")
    def scroll_to_element_e(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.log.debug("Scrolled to element")
        # wait for jquery
        self._wait_for_jQuery()

    @handle_exception(NoSuchElementException, "Element Not Found")
    def scroll_to_top_of_the_page(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

    @handle_exception(NoSuchElementException, "Element Not Found")
    def scroll_to_end_of_the_page(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)

    @handle_exception(NoSuchElementException, "Menu Element Not Found")
    def select_menu(self, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.perform()
        self.log.debug("Menu Item select with locator: {} and locatorType: {}".format(locator, locator_type))

    @handle_exception(NoSuchElementException, "Error Sending Raw Values")
    @handle_exception(WebDriverException, "WebDriver Exception Encountered")
    @handle_exception(AttributeError, "Attribute Exception Encountered")
    def send_raw_values(self, data, locator, locator_type="id", base_element=None):
        if base_element is None:
            element = self.get_element(locator, locator_type)
        else:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = base_element.find_element(by_type, locator)

        WebDriverWait(self.driver, self.default_wait_time).until(
            ec.visibility_of(element))
        self.high_light_element(element)

        element.clear()
        element.send_keys(str(data))
        self.log.debug("Send keys {} on locator: {} and locatorType: {}".format(data, locator, locator_type))

    @handle_exception(NoSuchElementException, "Cannot Send Keys on Element Not Found")
    @handle_exception(WebDriverException, "Cannot Send Keys to WebDriver")
    def send_key_to_driver(self, key: Keys):
        actions = ActionChains(self.driver)
        actions.send_keys(key).perform()

    @handle_exception(WebDriverException, "WebDriver Exception Encountered")
    @handle_exception(NoSuchWindowException, "No Such Window Exists")
    @handle_exception(NoSuchFrameException, "No Such Frame Exists")
    def switch_sub_frame(self, locators):
        self.driver.switch_to.default_content()
        for frame_locator in locators:
            self.driver.switch_to.frame(frame_locator)
            self.log.debug("Switched to sub frame with locator: {}".format(frame_locator))

    @handle_exception(WebDriverException, "WebDriver Exception Encountered")
    @handle_exception(NoSuchWindowException, "No Such Window Exists")
    @handle_exception(NoSuchFrameException, "No Such Frame Exists")
    def switch_frame_js(self, frame_name):
        #  frame = self.driver.execute_script("return top.window.document.getElementsByName('{}')".format(frame_name))
        #  self.driver.switch_to.default_content()
        #  self.driver.find_element.frame(frame)

        self.log.debug("Switched to frame with locator: {}".format(frame_name))

    def switch_frame(self, locator_type, locator):
        if locator_type is not None:
            ele = self.get_element(locator_type, locator)
            self.driver.switch_to.frame(ele)
        else:
            self._wait_for_javascript_func_("window.top.frames['{}'] != null".format(locator),
                                            self.default_wait_time)
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(locator)

        self.log.debug("Switched to frame with locator: {}".format(locator))

    def switch_child_frame(self, locator, locator_type="name"):
        # self.driver.switch_to.default_content()
        self.wait_for_element_to_appear(locator, locator_type)  # added this one as my machine fails to switch
        # frames because the screen is still loading?
        self.driver.switch_to.frame(locator)

        self.log.debug("Switched to frame with locator: {}".format(locator))

    def reload_frame(self, locator):
        self.driver.switch_to.default_content()
        self.driver.execute_script("window.frames['{}'].location.reload()".format(locator))
        self.log.debug("Reloaded frame with locator: {}".format(locator))

    @handle_exception(WebDriverException, "WebDriver Exception Encountered")
    @handle_exception(NoSuchWindowException, "No Such Window Exists")
    @handle_exception(NoSuchFrameException, "No Such Frame Exists")
    def switch_window(self, index, toggle_default=False):
        handles = self.driver.window_handles

        use_handle = handles[index]

        if toggle_default is False:
            pass
        else:
            self.driver.switch_to.default_content()

        self.driver.switch_to.window(use_handle)
        self.log.debug("Switched to window with locator: {}".format(use_handle))

    @handle_exception(WebDriverException, "WebDriver Exception Encountered")
    @handle_exception(NoSuchWindowException, "No Such Window Exists")
    @handle_exception(NoSuchFrameException, "No Such Frame Exists")
    def switch_child_window(self, index=None, toggle_default=False):

        handles = self.driver.window_handles

        if index is None:
            use_handle = handles[1]
        else:
            use_handle = handles[index]

        if toggle_default is False:
            pass
        else:
            self.driver.switch_to.default_content()

        self.driver.switch_to.window(use_handle)
        self.log.debug("Switched to window with locator: {}".format(use_handle))

    @handle_exception(NoSuchElementException, "Select Element Not Found")
    @handle_exception(NoSuchAttributeException, "Select Element Attribute Not Found")
    def select_by_option_value(self, value, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        # if not self.is_element_visible(locator):
        #     # this means we have to click its parent
        #     parent = self.get_parent_e(element)
        #     parent.click()
        self._wait_for_jQuery()
        self.high_light_element(element)
        select_elements = Select(element)
        select_elements.select_by_visible_text(str(value))
        self.log.debug("Select {} on locator: {}".format(value, locator))

    @handle_exception(NoSuchElementException, "Select Element Not Found")
    @handle_exception(NoSuchAttributeException, "Select Element Attribute Not Found")
    def select_by_option_value_e(self, value, element):
        self.high_light_element(element)
        select_elements = Select(element)
        select_elements.select_by_visible_text(value)

    @handle_exception(NoSuchElementException, "Select Element Not Found")
    @handle_exception(NoSuchAttributeException, "Select Element Attribute Not Found")
    def select_by_value(self, text, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        self._wait_for_jQuery()
        self.high_light_element(element)
        select_elements = Select(element)
        select_elements.select_by_visible_text(text)
        self.log.debug("Select {} on locator: {}".format(text, locator))

    @handle_exception(NoSuchElementException, "Element Not Found")
    def __get_select_element__(self, locator, locator_type="id") -> Select:
        element = self.get_element(locator, locator_type)
        self._wait_for_jQuery()
        self.high_light_element(element)
        return Select(element)

    @handle_exception(NoSuchElementException, "Select Element Not Found")
    @handle_exception(NoSuchAttributeException, "Select Element Attribute Not Found")
    def deselect_by_option_partial_text(self, partial_text, locator, locator_type="id"):
        # up here to not catch the exception raised by initial call
        select_elements = self.__get_select_element__(locator, locator_type)

        selected_item = next(iter([item for item in select_elements.options if partial_text in item.text]), None)

        if selected_item.is_selected():
            self.move_to_element_and_click_e(selected_item)

        self.log.debug("Deselect {} on locator: {}".format(partial_text, locator))

    @handle_exception(NoSuchElementException, "Select Element Not Found")
    @handle_exception(NoSuchAttributeException, "Select Element Attribute Not Found")
    def select_by_option_partial_text(self, partial_text, locator, locator_type="id"):
        select_elements = self.__get_select_element__(locator, locator_type)

        selected_item = next(iter([item for item in select_elements.options if partial_text in item.text]))

        if not selected_item.is_selected():
            self.move_to_element_and_click_e(selected_item)

        self.log.debug("Sselect {} on locator: {}".format(partial_text, locator))

    @handle_exception(NoSuchElementException, "Select Element Not Found")
    @handle_exception(NoSuchAttributeException, "Select Element Attribute Not Found")
    def select_by_option_text(self, text, locator_type="id", locator=""):
        element = self.get_element(locator, locator_type)
        # if not self.is_element_visible(locator):
        #     # this means we have to click its parent
        #     parent = self.get_parent_e(element)
        #     parent.click()
        self._wait_for_jQuery()
        self.high_light_element(element)
        select_elements = Select(element)
        select_elements.select_by_visible_text(text)

        self.log.debug("Select {} on locator: {}".format(text, locator))

    @handle_exception(NoSuchElementException, "Checkbox Element Not Found")
    @handle_exception(NoSuchAttributeException, "Checkbox Element Attribute Not Found")
    def select_checkbox(self, name, locator, locator_type="id", deselect=False):
        found_checkbox = False
        checkboxes = self.get_elements(locator, locator_type)
        for checkbox in checkboxes:
            if checkbox.get_attribute('name') == name:
                found_checkbox = True
                if not deselect and not checkbox.is_selected():
                    print(checkbox.is_selected())
                    print('Click to Select the checkbox ')
                    checkbox.click()
                if deselect and checkbox.is_selected():
                    print(checkbox.is_selected())
                    print('Click to Unselect the checkbox')
                    checkbox.click()
        if not found_checkbox:
            pass

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(ElementNotVisibleException, "Element Not Visible")
    @handle_exception(ElementNotSelectableException, "Element Disabled")
    def select_item(self, data, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        element.send_keys(data)
        self.log.debug("Send keys {} on locator: {} and locatorType: {}".format(data, locator, locator_type))

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    def get_element_attribute(self, element, attribute):
        return element.get_attribute(attribute)

    @handle_exception(NoSuchElementException, "Select Dropdown Not Found.")
    @handle_exception(ElementNotVisibleException, "Select Dropdown Is Not Visible.")
    def select_from_drop_down_by_text(self, text, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        if not self.is_element_visible(locator, locator_type):
            # this means we have to click its parent
            parent = self.get_parent_e(element)
            parent.click()
            self._wait_for_jQuery()
        select_elements = Select(element)
        chosen_option = next(iter(
            [item for item in select_elements.options if ((item.text or item.get_attribute("text")) == str(text))]),
            None)
        self.move_to_element_e(chosen_option)
        self.move_to_element_and_click_e(chosen_option)
        self._wait_for_jQuery()
        self.log.debug("Select {} on locator: {} and locatorType: {}".format(text, locator, locator_type))

    @handle_exception(NoSuchElementException, "Select Dropdown Not Found.")
    @handle_exception(ElementNotVisibleException, "Select Dropdown Is Not Visible.")
    def select_from_drop_down_by_value(self, value, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        if not self.is_element_visible(locator, locator_type):
            # this means we have to click its parent
            parent = self.get_parent_e(element)
            parent.click()
            self._wait_for_jQuery()
        select_elements = Select(element)
        chosen_option = next(iter(
            [item for item in select_elements.options if ((item.get_attribute("value")) == str(value))]),
            None)
        self.move_to_element_e(chosen_option)
        self.move_to_element_and_click_e(chosen_option)
        self._wait_for_jQuery()
        self.log.debug("Select {} on locator: {} and locatorType: {}".format(value, locator, locator_type))

    @handle_exception(NoSuchElementException, "Radio Element Not Found")
    @handle_exception(ElementNotVisibleException, "Radio Element Not Visible")
    @handle_exception(ElementNotSelectableException, "Radio Element Disabled")
    def select_radio_button(self, radio, throw_exception=False):
        self.high_light_element(radio)
        is_selected = self.is_element_selected_e(radio)

        if is_selected is False:
            self.move_to_element_and_click_e(radio)
        else:
            msg = "Radio button already set."
            if throw_exception is True:
                raise ElementNotSelectableException
            else:
                self.log.warn(msg)

    @handle_exception(NoSuchElementException, "Checkbox Element Not Found")
    @handle_exception(ElementNotVisibleException, "Checkbox Element Not Visible")
    @handle_exception(ElementNotSelectableException, "Checkbox Element Disabled")
    def toggle_checkbox(self, checkbox, toggle, throw_exception=False):
        self.high_light_element(checkbox)
        is_selected = self.is_element_selected_e(checkbox)

        if not is_selected and toggle:
            self.move_to_element_and_click_e(checkbox)

        elif is_selected and not toggle:
            self.move_to_element_and_click_e(checkbox)

        elif (not is_selected and not toggle) \
                or (is_selected and toggle):
            msg = "Checkbox already set."
            if throw_exception is True:
                raise ElementNotSelectableException
            else:
                self.log.warn(msg)

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(ElementNotVisibleException, "Element Not Visible")
    def verify_element(self, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(ElementNotVisibleException, "Element Not Visible")
    def verify_element_by_element(self, element):
        self.is_element_visible_e(element)
        self.high_light_element(element)

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(ElementNotVisibleException, "Element Not Visible")
    def verify_page_title(self, page_title):
        if page_title not in self.driver.title:
            raise AssertionError("ExpectedL {} Actual: {}".format(page_title, self.driver.title))

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def retrieve_element_attribute_value(self, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        if element is not None:
            self.high_light_element(element)
            return element.get_attribute("value")
        return None

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def verify_text_attribute_value(self, locator, locator_type="id", value=""):
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        if value not in element.get_attribute("value"):
            raise AssertionError("Expected: {} Actual: {}".format(value, element.get_attribute("value")))

    @handle_exception(ElementNotVisibleException, "Element Not Visible")
    @handle_exception(ElementNotSelectableException, "Element Disabled")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def verify_if_element_present_and_enabled(self, element):
        result = WebDriverWait(self.driver, self.default_wait_time).until(
            ec.visibility_of(element))
        return result and element.is_enabled()

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def retrieve_element_text(self, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        if element is not None:
            self.high_light_element(element)
            return element.text
        return None

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def verify_text(self, locator, locator_type="id", value=""):
        element = self.get_element(locator, locator_type)
        self.high_light_element(element)
        if value not in element.text:
            raise AssertionError("Expected: {} Actual: {}".format(value, element.text))

    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def verify_text_by_element(self, element, value):
        self.high_light_element(element)
        if value not in element.text:
            raise AssertionError("Expected: {} Actual: {}".format(value, element.text))

    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def verify_text_attribute_value_by_element(self, element, value=""):
        self.high_light_element(element)
        if value not in element.get_attribute("value"):
            raise AssertionError("Expected: {} Actual: {}".format(value, element.get_attribute("value")))

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def verify_text_attribute_value_as_float(self, locator, locator_type, value=""):
        expected = float(value)

        element = self.get_element(locator, locator_type)
        self.high_light_element(element)

        actual = float(element.get_attribute("value"))
        if expected != actual:
            raise AssertionError("Expected: {} Actual: {}".format(expected, actual))

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def verify_text_as_float(self, locator, locator_type, value):
        expected = float(value)

        element = self.get_element(locator, locator_type)
        self.high_light_element(element)

        actual = float(element.text)
        if expected != actual:
            raise AssertionError("Expected: {} Actual: {}".format(expected, actual))

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def wait_for_attribute_to_change(self, attribute_name, attribute_value, locator, locator_type="id",
                                     base_element=None):
        # get element first
        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        if base_element is None:
            element = self.driver.find_element(by_type, locator)
        else:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = base_element.find_element(by_type, locator)

        self.high_light_element(element)
        WebDriverWait(self.driver, self.default_wait_time).until(
            lambda driver: attribute_value not in element.get_attribute(attribute_name))
        self.log.debug("attribute changed from {}".format(attribute_value))

    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def wait_for_element_to_be_clickable(self, element):
        result = WebDriverWait(self.driver, self.default_wait_time).until(
            ec.visibility_of(element))
        if result and element.is_enabled():
            return element
        else:
            return False

    def wait_for_element_to_be_present(self, locator_type="id", locator="", timeout=15, poll_frequency=0.3):
        #  since there's preference to get the element first before
        #  checking if it's visible (which IMHO does not make sense)
        buffer = (0, self.get_element_buffer)[timeout is None]
        timeout = (timeout, self.default_wait_time)[timeout is None]
        timeout += buffer

        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            ec.presence_of_element_located((by_type, locator))) is not None

    @handle_exception(Exception, "All Exceptions Ignored", ignore_exception=True)
    def wait_for_multiple_elements_to_be_present(self, locator, locator_type="id", timeout=15, poll_frequency=0.3):
        #  since there's preference to get the element first before
        #  checking if it's visible (which IMHO does not make sense)
        buffer = (0, self.get_element_buffer)[timeout is None]
        timeout = (timeout, self.default_wait_time)[timeout is None]
        timeout += buffer

        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            ec.presence_of_all_elements_located((by_type, locator))) is not None

    @handle_exception(Exception, "All Exceptions Ignored", ignore_exception=True)
    def wait_for_element_to_be_visible(self, locator, locator_type="id", timeout=15, poll_frequency=0.3):
        #  since there's preference to get the element first before
        #  checking if it's visible (which IMHO does not make sense)
        buffer = (0, self.get_element_buffer)[timeout is None]
        timeout = (timeout, self.default_wait_time)[timeout is None]
        timeout += buffer

        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            ec.visibility_of_element_located((by_type, locator))) is not None

    def wait_for_element_to_be_visible_e(self, element, timeout=15, poll_frequency=0.3):
        #  since there's preference to get the element first before
        #  checking if it's visible (which IMHO does not make sense)
        buffer = (0, self.get_element_buffer)[timeout is None]
        timeout = (timeout, self.default_wait_time)[timeout is None]
        timeout += buffer

        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            ec.visibility_of(element)) is not None

    def wait_for_element_to_appear(self, locator, locator_type="id", timeout=15, poll_frequency=0.3):
        # DEEPT757
        # This method is designed to wait for the element to appear with poll frequency.
        # For each poll =0.3 sec it waits and verifies presence of element, if element present it stops
        # or else continues to loop till timeout
        # Please do not update this method for just waiting
        # For only wait use wait for page load  metho or other waits in the page
        # It throws error after maximum wait if the element doesn't appear.
        element = self.get_element(locator, locator_type)
        if WebDriverWait(self.driver, timeout, poll_frequency).until(
                ec.visibility_of(element)) is not None:
            return True

    def wait_for_element_to_appear_e(self, element, timeout=15, poll_frequency=0.3):
        if WebDriverWait(self.driver, timeout, poll_frequency).until(
                ec.visibility_of(element)) is not None:
            return True

    @handle_exception(Exception, "Wait For Element To Disappear Failed")
    def wait_for_element_to_disappear(self, locator, locator_type="id", timeout=None, poll_frequency=0.3):
        timeout = (timeout, self.default_wait_time)[timeout is None]
        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        WebDriverWait(self.driver, timeout, poll_frequency).until(
            ec.invisibility_of_element_located((by_type, locator)))
        self.log.debug("wait_for_element_to_disappear: locator:{} type:{}".format(locator, locator_type))

    def wait_for_element_to_disappear_e(self, element, timeout=None, poll_frequency=0.3):
        timeout = (timeout, self.default_wait_time)[timeout is None]
        WebDriverWait(self.driver, timeout, poll_frequency).until(
            ec.invisibility_of_element(element))

    @handle_exception(Exception, "Wait For Element To Be Stale Failed")
    def wait_for_element_to_be_stale(self, locator, locator_type="id", timeout=None, poll_frequency=0.3) -> bool:
        timeout = (timeout, self.default_wait_time)[timeout is None]

        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        element = self.get_element(by_type, locator)

        return self.wait_for_element_to_be_stale_e(element, timeout, poll_frequency)

    @handle_exception(Exception, "Wait For Element To Be Stale Failed", ignore_exception=True, return_condition=True)
    def wait_for_element_to_be_stale_e(self, element, timeout=None, poll_frequency=0.1) -> bool:
        timeout = (timeout, self.default_wait_time)[timeout is None]
        timeout += self.get_element_buffer

        self.log.debug("wait_for_element_to_be_stale")

        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            ec.staleness_of(element))

    @handle_exception(WebDriverException, "WebDriver Exception Encountered")
    @handle_exception(NoSuchWindowException, "No Such Window Exists")
    @handle_exception(NoSuchFrameException, "No Such Frame Exists")
    def wait_for_new_window_to_appear(self, expected_number_of_windows: int, timeout=None, poll_frequency=0.3) -> bool:
        timeout = (timeout, self.default_wait_time)[timeout is None]

        current_window_handles = self.driver.window_handles
        if len(current_window_handles) == expected_number_of_windows:
            return True
        print(current_window_handles)
        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            ec.new_window_is_opened(current_window_handles))

    def wait_for_page_to_load(self, time_sec=None):
        if time_sec is not None:
            time.sleep(time_sec)

        time_to_use = (time_sec, self.jquery_wait_time)[time_sec is None]
        try_limit = 10  # hardcoding, this is internal. This means it tries until document is ready
        i = 0
        result = False

        while i < try_limit and not result:
            i += 1
            try:
                result = WebDriverWait(self.driver, time_to_use).until(
                    lambda d: d.execute_script("return document.readyState=='complete'")
                )
            except:
                self.log.warn("Potential issue with slow loading - executed script on previous screen.")
                # this would recurse until document is in a ready state
                # recursion limit would be 1000 - hence would fail after 1000 retries.
                # we can change this by adding a counter

                # handle alerts first
                try:
                    if WebDriverWait(self.driver, 0.1).until(ec.alert_is_present()):
                        self.alert_accept()
                except:
                    ...

    def _wait_for_jQuery(self, time_sec=None):
        time_to_use = (time_sec, self.jquery_wait_time)[time_sec is None]

        # this is a fix for the error caused by waiting jquery stuff twice.
        # instead of consecutive calls, which appears to mess the driver out
        # we only use one call.
        WebDriverWait(self.driver, time_to_use).until(
            lambda d: d.execute_script(
                "return jQuery.active == 0 && $(':animated').length == 0")
        )
        self.log.debug("waiting for animations and for jquery complete")

    def _wait_for_javascript_func_(self, func_str: str, time_sec=None):
        time_to_use = (time_sec, self.jquery_wait_time)[time_sec is None]
        func_str = func_str.replace("return", "")
        func_str = func_str.lstrip(" ").rstrip(" ")

        # this is a fix for the error caused by waiting jquery stuff twice.
        # instead of consecutive calls, which appears to mess the driver out
        # we only use one call.
        WebDriverWait(self.driver, time_to_use).until(
            lambda d: d.execute_script(
                "return {}".format(func_str))
        )
        self.log.debug("js_cowaiting for {} time={}".format(func_str, time_to_use))
        return True

    def _pause(self):
        time.sleep(self.get_element_buffer)

    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(ElementNotVisibleException, "Element Not Visible")
    @handle_exception(ElementNotSelectableException, "Element Disabled")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def set_wait_for_element_to_be_clickable(self, locator, locator_type="id", default_wait_time=10):
        # This waits up to 10 seconds before throwing a TimeoutException.
        # WebDriverWait by default calls the ExpectedCondition every 500 milliseconds until it returns successfully.
        element = self.get_element(locator, locator_type)
        result = WebDriverWait(self.driver, default_wait_time).until(
            ec.visibility_of(element))
        if result and element.is_enabled():
            return element
        else:
            return False

    @handle_exception(WebDriverException, "WebDriver Exception Encountered")
    @handle_exception(NoSuchWindowException, "No Such Window Exists")
    @handle_exception(NoSuchFrameException, "No Such Frame Exists")
    def get_current_frame(self):
        frame_name = self.driver.execute_script("return self.name")
        return frame_name

    @handle_exception(WebDriverException, "WebDriver Exception Encountered")
    @handle_exception(NoSuchWindowException, "No Such Window Exists")
    @handle_exception(NoSuchFrameException, "No Such Frame Exists")
    def get_current_window_handler(self):
        window_name = self.driver.current_window_handle
        return window_name

    #  below method can be used for extracting the data from the screen where the displayed text is
    @handle_exception(NoSuchElementException, "Element Not Found")
    @handle_exception(ElementNotVisibleException, "Element Not Visible")
    @handle_exception(ElementNotSelectableException, "Element Disabled")
    @handle_exception(NoSuchAttributeException, "Element Attribute Not Found")
    @handle_exception(AttributeError, "Element Attribute Exception Encountered")
    def get_select_element_active_text(self, locator, locator_type="id"):
        element = self.get_element(locator, locator_type)
        self._wait_for_jQuery()
        self.high_light_element(element)
        select_elements = Select(element)
        ret_val = select_elements.first_selected_option.text
        self.log.debug(
            "Selected option {} on locator: {} and locatorType: {}".format(ret_val, locator, locator_type))
        return ret_val

    @handle_exception(NoSuchElementException, "Radio Element Not Found")
    @handle_exception(ElementNotVisibleException, "Radio Element Not Visible")
    @handle_exception(ElementNotSelectableException, "Radio Element Disabled")
    @handle_exception(NoSuchAttributeException, "Radio Element Attribute Not Found")
    @handle_exception(AttributeError, "Radio Element Attribute Exception Encountered")
    def toggle_radio_button(self, option):
        self.element_click("//td[contains(text(), '{}')]//input".format(option), "xpath")

    @handle_exception(NoAlertPresentException, "Alert Not Found", ignore_exception=True, return_condition=False)
    @handle_exception(WebDriverException, "WebDriver Exception Encountered", ignore_exception=True,
                      return_condition=False)
    def is_alert_present(self, time_sleep=2):

        WebDriverWait(self.driver, time_sleep).until(ec.alert_is_present(),
                                                     'Timed out waiting for alert')
        alert = self.driver.switch_to_alert()

        return alert.text

    @handle_exception(NoAlertPresentException, "Alert Not Found", ignore_exception=True)
    @handle_exception(WebDriverException, "WebDriver Exception Encountered", ignore_exception=True)
    def alert_accept(self, time_sleep=1):

        alert = self.driver.switch_to_alert()

        alert.accept()
        time.sleep(time_sleep)
        return True

    @handle_exception(NoAlertPresentException, "Alert Not Found", ignore_exception=True)
    @handle_exception(WebDriverException, "WebDriver Exception Encountered", ignore_exception=True)
    def alert_get_text(self, time_sleep=1, accept=True):

        alert = self.driver.switch_to_alert()
        text = alert.text
        if accept:
            alert.accept()
        time.sleep(time_sleep)
        return text

    @handle_exception(Exception, "Button Post Check Ignored Exception", ignore_exception=True)
    def _button_post_check_(self, element, time_sec=None):
        e_check = False

        if element.parent is not None and not self.wait_for_element_to_be_stale_e(element.parent, time_sec):
            self.wait_for_element_to_be_stale_e(element.parent,
                                                max(0.1, self.default_wait_time - self.get_element_buffer))
            e_check = True
        if not e_check and not self.wait_for_element_to_be_stale_e(element, time_sec):
            self.wait_for_element_to_be_stale_e(element, max(0.1, self.default_wait_time - self.get_element_buffer))

    @handle_exception(WebDriverException, "WebDriver Exception Encountered")
    @handle_exception(NoSuchWindowException, "No Such Window Exists")
    def is_window_open(self, index=None):
        handles = self.driver.window_handles
        if index is None:
            return True
        elif int(index) >= len(handles):
            self.log.debug("Window with index {} is currently not open".format(index))
            return False
        else:
            return True

    @handle_exception(WebDriverException, "WebDriver Exception Encountered on Saving Downloads")
    def save_file_to_downloads(self, download_folder, destination_filename=None):
        """

        :param download_folder: Folder location to download file
        :param destination_filename: Optional parameter to rename source filename
        :return:
        """
        timeout = 300
        if download_folder not in (None, "None"):
            # get the first file in the download folder
            source_filename = max([f for f in os.listdir(download_folder)],
                                  key=lambda file: os.path.getctime((os.path.join(download_folder, file))))
            while timeout > 0:
                # check if filename still partially downloaded, if so be in loop
                if '.part' in source_filename:
                    time.sleep(30)
                    timeout = timeout - 30
                else:
                    if destination_filename is not None:
                        os.rename(os.path.join(download_folder, source_filename),
                                  os.path.join(download_folder, destination_filename))
                        self.log.info(f"\nFile downloaded to location {download_folder} "
                                      f"with filename {destination_filename}\n")
                    else:
                        self.log.info(
                            f"\nFile downloaded to location {download_folder} with filename {source_filename}\n")
                    break
        else:
            self.log.info("\nUnable to download file since download folder not specified\n")

    def hover_menu(self, element):
        """
        Mouse Hover Menu name
        :param locator:
        :param locator_type:
        :return:
        """

        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.perform()

