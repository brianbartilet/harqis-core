import sys, json
from pathlib import Path
from typing import Any, Optional
from utilities.logging.custom_logger import create_logger

from utilities.data.json import JsonObject
from utilities.contracts.file import IFileLoader

from typing import TypeVar

T = TypeVar('T')

log = create_logger("GQL File Loader")

class ResourceFileGql(IFileLoader):
    def __init__(self, **kwargs):
        super(ResourceFileGql, self).__init__(**kwargs)
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.variables: T = kwargs.get('variables', {})

    def load(self) -> any:
        file_path = self.find_file_from_base_path()
        try:
            with open(file_path, 'r', encoding=self.encoding) as resource:
                s = resource.read()
                if isinstance(self.variables, object):
                    self.variables = self.variables.__dict__
                    data = {"query": s, "variables": self.variables}
        except FileNotFoundError as e:
            sys.exit(f"Terminating application .gql file not loaded due to {e}.")

        return data


