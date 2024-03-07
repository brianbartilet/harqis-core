import csv
import os

from reports.report_generator import ReportGenerator


class CsvReportGenerator(ReportGenerator):

    def __init__(self):
        super(CsvReportGenerator, self).__init__(delimiter = csv.excel_tab.delimiter)

    def write_report(self):
        # generate our path
        self._create_path_to_file_()

        full_path = os.path.join(self._output_dir, self._output_filename)

        if not full_path.endswith('.csv'):
            full_path = "{}.csv".format(full_path)

        # create / open our file:
        with open(full_path, 'w',  encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')

            # write the status
            self.__write_result__(writer)

            # write any tags
            self.__write_tags__(writer)

            # write the scenario file first
            self.__write_scenario_description__(writer)

            # write the headers if any
            self.__write_headers__(writer)

            # write the results if any
            self.__write_result_data__(writer)

        # dispose our self in case someone accidentally reuses us
        self._clear_vars_()

    def __write_result__(self, writer):
        if self._result is not None:
            writer.writerow([self._result])
            writer.writerow('')

    def __write_tags__(self, writer):
        if len(self._tags) > 0:
            writer.writerow(["TAGS:"] + self._tags)

            # write a blank line
            writer.writerow('')

    def __write_scenario_description__(self, writer):

        if self._scenario_description is not None:
            if not isinstance(self._scenario_description, list):
                # this is a raw string, and we must process it accordingly
                temp_description = []
                for row in str(self._scenario_description).split('\n'):
                    temp_description.append([row])
                self._scenario_description = temp_description

            for desc in self._scenario_description:
                if not isinstance(desc, list):
                    desc = [desc]
                writer.writerow(desc)

            # write a blank line
            writer.writerow('')

    def __write_headers__(self, writer):
        if self._headers is not None:
            if not isinstance(self._headers, list) and isinstance(self._headers, str):
                self._headers = self._headers.split(',')
            writer.writerow(self._headers)

    def __write_result_data__(self, writer):
        if self._row_data is not None:
            writer.writerow(["What we've checked"])
            for row in self._row_data:
                if not isinstance(row, list) and isinstance(row, str):
                    row = row.split(',')

                writer.writerow(row)