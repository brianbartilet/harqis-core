import argparse

from core.codegen.mustache.generators.rest.generate import ServiceTestGeneratorRest


if __name__ == '__main__':
    #  region Create the argument parser
    parser = argparse.ArgumentParser(description='Converts OpenAPI specs to test cases')
    parser.add_argument('--spec', type=str, default="tasks_api_specs.yaml",
                        help='The OpenAPI specifications file can be a YAML, JSON or URL')
    #  endregion

    #  region Run Generated Code using Mustache
    generator = ServiceTestGeneratorRest(source=parser.parse_args().spec)
    data = generator.load_source()

    generator.create_directories()
    generator.parse_spec(data)
    generator.write_files()
    #  endregion
