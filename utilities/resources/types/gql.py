from utilities.contracts.file import IFileLoader

from typing import TypeVar

T = TypeVar('T')


class ResourceFileGql(IFileLoader):
    def __init__(self, **kwargs):
        super(ResourceFileGql, self).__init__(file_extension='.gql', **kwargs)

        self.encoding = kwargs.get('encoding', 'utf-8')
        self.variables: T = kwargs.get('variables', {})

    def load(self) -> any:
        file_path = self.find_file_from_base_path()
        try:
            with open(file_path, 'r', encoding=self.encoding) as resource:
                s = resource.read()
                data = {"query": s, "variables": self.variables}
        except FileNotFoundError as e:
            self.log.error(f"GQL file not loaded due to {e}.")

        return data


