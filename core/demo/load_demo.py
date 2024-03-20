import shutil
import os
import yaml

# RUN THIS ONLY IN DEMO PROJECT https://github.com/brianbartilet/harqis-demo-testing


def create_and_move_yaml(filename: str, data: dict, destination):
    # Create the YAML file with content
    with open(filename, 'w') as file:
        yaml.dump(data, file)

    # Move the file to the destination
    shutil.move(filename, os.path.join(destination, filename))
    print(f"{filename} has been moved to {destination}")


def create_demo_configurations():

    # Create the config.yaml file for the __template_tests_services_graphql
    config_template_rest = {
        "__template_tests_services_rest": {
            "client": "rest",
            "parameters": {
                "base_url": "https://jsonplaceholder.typicode.com/",
                "response_encoding": "utf-8",
                "verify": True
            }
        }
    }
    create_and_move_yaml("config.yaml", config_template_rest,
                         os.path.join(os.getcwd(),
                                      "demo",
                                      "testing",
                                      "__template_tests_services_rest"))

    # Create the config.yaml file for the __template_tests_services_graphql
    config_template_graph = {
        "__template_tests_services_graphql": {
            "client": "graphql",
            "parameters": {
                "base_url": "https://graphql.anilist.co/",
                "response_encoding": "utf-8",
                "verify": True
            }
        }
    }
    create_and_move_yaml("config.yaml", config_template_rest,
                         os.path.join(os.getcwd(),
                                      "demo",
                                      "testing",
                                      "__template_tests_services_graphql"))