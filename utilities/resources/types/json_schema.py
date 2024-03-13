import json
from utilities.contracts.file import IFileLoader
from typing import TypeVar, Any
from jsonschema import validate, ValidationError
from json.decoder import JSONDecodeError

T = TypeVar('T')


class ResourceFileJsonSchema(IFileLoader):
    def __init__(self, **kwargs):
        super(ResourceFileJsonSchema, self).__init__(**kwargs)
        self.encoding = kwargs.get('encoding', 'utf-8')

    def load(self) -> Any:
        file_path = self.find_file_from_base_path()
        if file_path is None:
            raise FileNotFoundError
        try:
            with open(file_path, 'r', encoding=self.encoding) as resource:
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
            
