import argparse
import unittest
from core.config.env_variables import Environment, ENV
from core.apps.mustache.generators.rest.generate import TestGeneratorServiceRest


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


@unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
def test_runner():
    spec = "tasks_api_specs.yaml"
    gen = TestGeneratorServiceRest(source=spec)

    source = gen.load_source()
    gen.create_directories()
    gen.parse_spec(source)
    gen.write_files()


@unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
def test_runner_url():
    url = "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore-expanded.yaml"
    gen = TestGeneratorServiceRest(source=url)

    source = gen.load_source()
    gen.create_directories()
    gen.parse_spec(source)
    gen.write_files()


