from web.browser.selenium_driver import *
from utilities import *

from behave.model import Table

from utilities.apps_context import AppConfigurationContext
from web.services.core.contracts.constants.service_client_type import ServiceClientType
from abc import abstractmethod

class BasePage(SeleniumDriver):

    @abstractmethod
    def __init__(self,
                 driver,
                 source_id: str,
                 apps_config_data: dict,
                 app_ctx: type = AppConfigurationContext,
                 **kwargs):

        self.app_ctx = app_ctx(source_id, ServiceClientType.WEBDRIVER, apps_config_data)
        self.source_id = source_id
        self.parameters = self.app_ctx.load_app_parameters()

        self.base_url = self.parameters.get('base_url', None)
        self.url = self.parameters.get('url', None)

        self.id = kwargs.get('id', None)
        self.title = kwargs.get('title', None)
        self.page_id = kwargs.get('page_id', None)
        self.kwargs = kwargs

        super().__init__(driver)

    def assert_that(self, arg1, arg2, arg3='Checkpoint Failed.'):
        try:
            assert_that(arg1=arg1, arg2=arg2, arg3=arg3)
        except AssertionError as error:
            self.log.error(str(error).replace("\n", ""))
            raise error

    def merge_data_dictionaries(self, dic_x, dic_y):
        data = OrderedDict(dic_x.copy())
        data.update(dic_y)

        return data

    def set_fields_from_data(self, target_loc_dic, skip_keys=None, use_loc_dic=None, sorted_keys=None):
        """ set fields from a dictionary key value pair information using the locator dictionary.

        :param target_loc_dic: dictionary data to contain information
        :param skip_keys: list of keys to remove from previous processing
        :param use_loc_dic: use custom locator dictionary aside from page defined
        :param sorted_keys: list of keys to be executed in an order from the defined dic
        """
        if sorted_keys is not None:
            sorted_l = list((i, target_loc_dic.get(i)) for i in sorted_keys)
            sorted_d = OrderedDict()

            for item in sorted_l:
                sorted_d[item[0]] = item[1]

            for key in sorted_d:
                if key in target_loc_dic:
                    del target_loc_dic[key]

            dic = self.merge_data_dictionaries(sorted_d, target_loc_dic)
        else:
            dic = target_loc_dic

        if use_loc_dic is not None:
            loc_dic = use_loc_dic
        else:
            loc_dic = self.locator_dictionary

        for key in dic:
            if skip_keys is not None:
                if key in skip_keys:
                    continue
            try:
                if dic[key] is None: continue
                self.log.info("Setting data information on " + key + " element")

                elements = self.get_elements(*loc_dic[key])
                if len(elements) > 0:
                    element = next((e for e in elements))
                    self.high_light_element(element)
                    if element.get_attribute('type') == 'text':
                        element.clear()
                        element.send_keys(dic[key])
                    elif element.get_attribute('type') == 'radio':
                        self.select_radio_button(element)
                    elif element.get_attribute('type') == 'checkbox':
                        self.toggle_checkbox(element, bool(dic[key]))
                    elif element.get_attribute('type') == 'select' or element.tag_name == 'select':
                        self.select_by_option_value_e(str(dic[key]), element)
                    else:
                        pass
                        # self.move_to_element_and_click_e(element)
                else:
                    pass
            except:
                self.log.warn("Unable to set field on " + key)

    def get_table_body_rows(self, table_id=None, t_body_tag=1):
        '''
        :param table_id: optional, table element
        :param t_body_tag: optional, target body element
        :return: All td elements in the table grouped into lists
        e.g.    Row1 (Cell_1, Cell_2, Cell_3, ...)
                Row2 (Cell_1, Cell_2, Cell_3, ...)
                Row3 (Cell_1, Cell_2, Cell_3, ...)
                ...
        '''
        if table_id is None:
            table_id = self.driver.find_element(By.XPATH, '//table')

        t_body = table_id.find_element(By.CSS_SELECTOR, 'tbody:nth-of-type(' + str(t_body_tag) + ')')

        body_rows = t_body.find_elements(By.TAG_NAME, "tr")
        row_list = [x.find_elements(By.TAG_NAME, "td") for x in body_rows]

        return row_list

    def get_table_data(self, table_id=None):
        headings = self.get_table_header(table_id)
        rows = self.get_table_body_rows(table_id)

        table_heading = [heading.text for heading in headings]
        data = []
        for item in rows:
            row_data = []
            for cell in item:
                row_data.append(cell.text.strip())
            data.append(row_data)
        return Table(table_heading, line=0, rows=data)

    def get_table_header(self, table_id=None):
        if table_id is None:
            table_id = self.driver.find_element(By.XPATH, '//table')
        thead = table_id.find_element(By.TAG_NAME, "thead")
        heading_rows = thead.find_elements(By.TAG_NAME, "td")
        if len(heading_rows) == 0:
            # search for the other elements
            heading_rows = thead.find_elements(By.TAG_NAME, "th")

        return heading_rows

    def get_table_data_withspaces(self, table_id=None, t_body_tag=1):
        headings = self.get_table_header(table_id)
        rows = self.get_table_body_rows(table_id, t_body_tag)

        table_headings = [heading.text for heading in headings]
        data = []
        for item in rows:
            row_data = []
            for cell in item:
                data_items = cell.text.strip()
                if data_items == '':
                    data_items = ' '
                row_data.append(data_items)
            data.append(row_data)

        return Table(table_headings, line=0, rows=data)

    def get_table_data_when_structure_provided(self, table_structure, table_id=None, t_body_tag=1):
        """get table data from the page in to a behave Table object based on enum values in formdetails."""
        table_heading = []

        if table_id is None:
            table_id = self.driver.find_element(By.XPATH, '//table')

        tbody = table_id.find_element(By.XPATH, 'tbody[' + str(t_body_tag) + ']')

        for heading in table_structure:
            table_heading.append(heading.name)

        body_rows = tbody.find_elements(By.TAG_NAME, "tr")
        data = []

        for row in body_rows:
            row_data = []
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= len(table_heading):
                for heading in table_structure:
                    row_data.append(cols[heading.value].text.strip())
                data.append(row_data)

        return Table(table_heading, line=0, rows=data)

    def re_structure_table_data(self, expectedtable, actualtable, formdetails):
        """re-structure table data based on the required columns from expected table."""
        table_heading = []
        for heading in expectedtable.headings:
            table_heading.append(heading)

        table_data = []
        for row in actualtable.rows:
            col_index = 0
            row_item = []
            for col in row:
                if actualtable.headings[col_index] in expectedtable.headings:
                    for names in formdetails:
                        if names.name == actualtable.headings[col_index]:
                            row_item.append(row[names.value])
                            break
                col_index += 1
            table_data.append(row_item)

        return Table(table_heading, 0, table_data)

    @abstractmethod
    def get_table_text_value(self, key):
        self.log.warn("retrieve_data_value_for_validation called get_table_text_value without concrete implementation")

    @abstractmethod
    def get_table_text_indexed_column_value(self, key, index=2):
        self.log.warn(
            "retrieve_data_value_for_validation called get_table_text_indexed_column_value without concrete implementation")

    @abstractmethod
    def wait_page_to_load(self, *args):
        super().wait_for_page_to_load(*args)

    @abstractmethod
    def did_page_load(self, *args):
        ...

    @abstractmethod
    def navigate_to_page(self, *args):
        ...

    @abstractmethod
    def login(self, *args):
        ...

    @abstractmethod
    def logout(self):
        ...
