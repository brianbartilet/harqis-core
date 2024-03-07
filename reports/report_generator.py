import abc
import os

class ReportGenerator():

    def __init__(self, delimiter):
        self._delimiter = delimiter
        self._clear_vars_()


    @abc.abstractmethod
    def write_report(self):
        """
        This opens the report, writes whatever we stored, and closes the handle
        This was done so that we don't keep a file handle open
        :return:
        """

    def set_output_dir(self, path):
        # can write something here to clean the path but for now let's keep it this way
        self._output_dir = path

    def set_output_filename(self, filename):
        # can write something here to clean the path but for now let's keep it this way
        self._output_filename = filename

    def set_scenario_description(self, scenario_description):
        if self._scenario_description is None:
            self._scenario_description = scenario_description
        else:
            raise AttributeError("self.__scenario_description already defined.")

    def add_tags(self, tags : list):
        self._tags.extend(tags)

    def set_header(self, header_data):
        if self._headers is None:
            self._headers = header_data
        else:
            raise AttributeError("self.__headers already defined.")

    def set_result(self, result_string):
        if self._result is None:
            self._result = result_string
        else:
            raise AttributeError("self._result already defined.")

    def append_row(self, row_data):
        if row_data is not None:
            if not isinstance(row_data, list):
                row_data = [row_data]
            self._row_data.append(row_data)


    def _create_path_to_file_(self):
        if self._output_dir is None:
            raise AttributeError("self.__output_dir not yet defined.")

        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)

    def _clear_vars_(self):
        self._headers = []
        self._output_dir = None
        self._output_filename = None
        self._scenario_description = None
        self._result = None
        self._row_data = []
        self._tags = []