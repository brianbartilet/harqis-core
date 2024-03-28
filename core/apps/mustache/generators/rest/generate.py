import os
import yaml
import json
import validators
import pystache

from typing import Dict
from urllib.parse import urlparse

from core.utilities.resources.download_file import ServiceDownloadFile
from core.utilities.logging.custom_logger import create_logger
from core.utilities.data.strings import convert_to_snake_case, remove_special_chars
from core.utilities.path import get_module_from_file_path

from core.apps.mustache.contracts.generator import IGenerator
from apps.mustache.generators.rest.open_api_helpers import transform_types, transform_paths, transform_models, \
    group_paths_by_resource

from core.apps.mustache.generators.rest.templates import GENERATOR_PATH_REST
from core.apps.mustache.generators.rest.variables.models import MustacheTemplateModel
from core.apps.mustache.generators.rest.variables.service import MustacheTemplateService


class TestGeneratorServiceRest(IGenerator):

    def __init__(self, source: str, base_path: str = os.getcwd()):
        super().__init__(source=source, base_path=base_path)

        self.log = create_logger(self.__class__.__name__)
        self.source: str = source
        self.file_name: str = ''
        self.files: Dict[str, str] = {}  # key: file_path, value: content
        self.initialize_directories(base_path)
        self.initialize_templates()

    def initialize_directories(self, base_path: str):
        """Sets up directories based on the base path."""
        self.directories['specs'] = os.path.join(base_path, 'specs')
        self.directories['generated'] = os.path.join(base_path, 'generated')

        gen_dirs = ['models', 'services', 'tests',
                    'tests.sanity', 'tests.integration', 'tests.negative']

        self.directories = {**self.directories,
                            **{d: os.path.join(self.directories['generated'], *d.split('.')) for d in gen_dirs}}

    def initialize_templates(self):
        """Sets up template file paths."""
        self.templates = {name: os.path.join(GENERATOR_PATH_REST, f"{name}.mustache")
                          for name in ['base_service', 'config', 'models', 'service', 'test']}

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
            self.file_name = os.path.basename(url_path)
            downloader.download_file(file_name=self.file_name, path=base_path)
        else:
            self.file_name = self.source

        file_path = os.path.join(base_path, self.file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as file:
            if self.source.endswith('.yaml'):
                return yaml.load(file, Loader=yaml.FullLoader)
            if self.source.endswith('.json'):
                return json.load(file)
            else:
                raise Exception("Unsupported file format")

    def parse_spec(self, source_data: dict) -> None:
        """
        Parse the OpenAPI spec
        Args:
            source_data {dict} - The OpenAPI spec
        """
        renderer = pystache.Renderer()

        #  region Generate Base Service

        template_base = self.templates['base_service']
        self.files[os.path.join(self.directories['generated'], "base_service.py")] = (
            renderer.render_path(template_base, {}))

        #  endregion

        #  region Generate Config

        template_base = self.templates['config']
        self.files[os.path.join(self.directories['generated'], "config.py")] = (
            renderer.render_path(template_base, {}))

        #  endregion

        #  region Generate Models

        source_model = source_data['components']['schemas']
        template_model = self.templates['models']
        for key, value in source_model.items():
            if 'allOf' in value.keys():
                continue
            else:
                properties = transform_types(value['properties'])
                transform_properties = [
                    {"name": p, "type": v['type'],
                     **({"example": v['example']} if "example" in v else {'example': None})}
                    for p, v in properties.items()
                ]
                prepare = MustacheTemplateModel(object_name=key, properties=transform_properties)
                self.files[os.path.join(self.directories['models'], f"{convert_to_snake_case(key)}.py")] = (
                    renderer.render_path(template_model, prepare.get_dict()))

        # endregion

        #  region Generate Services
        paths_by_resource = group_paths_by_resource(source_data['paths'])
        base_module_path_models = get_module_from_file_path(self.directories['models'])
        base_module_path_services = get_module_from_file_path(self.directories['generated'])
        for resource in paths_by_resource.keys():
            models = transform_models(paths_by_resource[resource])
            operations = transform_paths(paths_by_resource[resource])
            prepare = MustacheTemplateService(base_module_path_services=base_module_path_services,
                                              base_module_path_models=base_module_path_models,
                                              models=models,
                                              operations=operations,
                                              resource=remove_special_chars(resource).capitalize())

            template_base = self.templates['service']
            key = os.path.join(self.directories['services'], f"{remove_special_chars(resource)}.py")
            self.files[key] = (
                renderer.render_path(template_base, prepare))

        #  endregion

    def create_directories(self) -> None:
        super().create_directories()

    def write_files(self) -> None:
        super().write_files(except_keys=['specs', ])
