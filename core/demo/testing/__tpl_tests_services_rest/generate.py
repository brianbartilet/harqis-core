import argparse
import os
import yaml
import json
import validators
import pystache

from typing import Dict
from urllib.parse import urlparse

from core.utilities.resources.download_file import ServiceDownloadFile
from core.utilities.logging.custom_logger import create_logger
from core.utilities.data.objects import convert_to_snake_case

from demo.testing.__tpl_tests_services_rest.generators.variables.tpl_dto import MustacheTemplate


class TestGeneratorServiceRest:

    def __init__(self, source: str, base_path: str = os.getcwd()):
        self.log = create_logger(self.__class__.__name__)
        self.source: str = source
        self.file_name: str = ''
        self.files: Dict[str, str] = {}  # key: file_path, value: content
        self.directories: Dict[str, str] = {
            'specs': os.path.join(base_path, '.specs'),
            'generators': os.path.join(base_path, 'generators'),
            'generated': os.path.join(base_path, 'generated'),
            'dto': os.path.join(base_path, 'generated', 'dto'),
            'services': os.path.join(base_path, 'generated', 'services'),
            'tests': os.path.join(base_path, 'generated', 'tests'),
            'tests.sanity': os.path.join(base_path, 'generated', 'tests', 'sanity'),
            'tests.integration': os.path.join(base_path, 'generated', 'tests', 'integration'),
            'tests.negative': os.path.join(base_path, 'generated', 'tests', 'negative'),
        }

        self.templates: Dict[str, str] = {
            'base_service': os.path.join(self.directories['generators'], 'tpl_base_service.mustache'),
            'config': os.path.join(self.directories['generators'], 'tpl_config.mustache'),
            'dto': os.path.join(self.directories['generators'], 'tpl_dto.mustache'),
            'service': os.path.join(self.directories['generators'], 'tpl_service.mustache'),
            'test': os.path.join(self.directories['generators'], 'tpl_test.mustache'),
        }

    def load_source(self) -> dict:
        """
        Load a OpenAPI source to a JSON object
        Args:
            source {str} - The name of the file
            base_path {str} - The base path of the file
        """
        base_path = self.directories['specs']

        if validators.url(self.source):
            downloader = ServiceDownloadFile(url=self.source)
            url_path = urlparse(self.source).path
            self.source = os.path.basename(url_path)
            downloader.download_file(file_name=self.file_name, path=base_path)

        file_path = os.path.join(base_path, self.source)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as file:

            if self.source.endswith('.yaml'):
                return yaml.load(file, Loader=yaml.FullLoader)
            if self.source.endswith('.json'):
                return json.load(file)
            else:
                raise Exception("Unsupported file format")

    def create_directories(self) -> None:
        """
        Create the directories from the directories dictionary
        """
        for directory in self.directories.values():
            if not os.path.exists(directory):
                os.makedirs(directory)

    def parse_spec(self, source_data: dict) -> None:
        """
        Parse the OpenAPI spec
        Args:
            data {dict} - The OpenAPI spec
        """
        renderer = pystache.Renderer()

        #  region Create Models

        source_dto = source_data['components']['schemas']
        template_dto = self.templates['dto']
        for key, value in source_dto.items():
            properties = value['properties']
            transform_properties = [{"name": p, "type": v['type'], "example": v['example']}
                                    for p, v in properties.items()]
            transform_key = key
            prepare = MustacheTemplate(object_name=transform_key, properties=transform_properties)
            self.files[os.path.join(self.directories['dto'], f"{convert_to_snake_case(key)}.py")] = (
                renderer.render_path(template_dto, prepare.get_dict()))

        # endregion

    def write_files(self) -> None:
        """
        Write the files
        Args:
            data {dict} - The OpenAPI spec
        """
        for key in self.files.keys():
            with open(key, 'w') as file:
                file.write(self.files[key])


if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Converts OpenAPI specs to test cases')
    parser.add_argument('--spec', type=str, default="open_api.yaml",
                        help='The OpenAPI specifications file can be a YAML, JSON or URL')
    generator = TestGeneratorServiceRest(source=parser.parse_args().spec)

    data = generator.load_source()

    generator.create_directories()

    generator.parse_spec(data)

    generator.write_files()


def test_run():
    g = TestGeneratorServiceRest(source="tasks_api_specs.yaml")
    data = g.load_source()
    g.create_directories()
    g.parse_spec(data)
    g.write_files()

