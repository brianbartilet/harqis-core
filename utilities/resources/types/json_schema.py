import json

from utilities.contracts.file import IFileLoader
from typing import Any
from jsonschema import validate, ValidationError
from json.decoder import JSONDecodeError


class ResourceFileJsonSchema(IFileLoader):
    def __init__(self, **kwargs):
        super(ResourceFileJsonSchema, self).__init__(**kwargs)
        self.encoding = kwargs.get('encoding', 'utf-8')

    def load(self) -> Any:
        try:
            with open(self.full_path_to_file, 'r', encoding=self.encoding) as resource:
                s = json.load(resource)
                return s
        except FileNotFoundError as e:
            self.log.error(f"JSON schema file not loaded due to {e}.")
            raise
        except JSONDecodeError as e:
            self.log.error(f"Invalid JSON format in schema file: {e}")
            raise

    def validate(self, data: dict) -> bool:
        schema = self.load()
        try:
            validate(instance=data, schema=schema)
            return True
        except ValidationError as e:
            self.log.error(f"JSON data validation failed: {e}")
            return False
            
