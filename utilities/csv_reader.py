import csv
from typing import TypeVar, Generic, Type
from typing import List
from utilities.custom_logger import custom_logger

T = TypeVar('T')
log = custom_logger("CSV_READER")


def generate_objects_from_csv_data(csv_file_path, kls_hook: Type[T], start_row=0, **kwargs) -> List[Type[T]]:
    return_data = []
    headers = []

    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == start_row:
                headers = row
                log.info('Column names are {0}'.format(", ".join(row)))
                line_count += 1
            else:
                line_count += 1
                #  loop rows here to push in object properties
                args = {}
                for index, header in enumerate(headers):
                    args[str(header).lower()] = row[index]
                return_data.append(kls_hook(**args, **kwargs))

        log.info('Processed {0} data rows.'.format(line_count - 1))

    return return_data