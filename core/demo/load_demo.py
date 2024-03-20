import shutil
import os
import yaml

# RUN THIS ONLY IN DEMO PROJECT https://github.com/brianbartilet/harqis-demo-testing

def copy_directory(source_dir, target_dir):
    try:
        # Check if the target directory already exists
        if os.path.exists(target_dir):
            # If it exists, remove it to avoid errors
            shutil.rmtree(target_dir)
        # Copy the source directory to the target directory
        shutil.copytree(source_dir, target_dir)
        print(f"Directory {source_dir} copied to {target_dir} successfully.")
    except Exception as e:
        print(f"Error copying directory: {e}")


def create_and_move_yaml(filename, data: dict, destination):
    # Create the YAML file with content
    with open(filename, 'w') as file:
        yaml.dump(data, file)

    # Move the file to the destination
    shutil.move(filename, os.path.join(destination, filename))
    print(f"{filename} has been moved to {destination}")


if __name__ == "__main__":
    # Specify the source and target directories
    source_directory = os.path.join(os.getcwd(), "venv",
                                                 "lib",
                                                 "site-packages",
                                                 "core",
                                                 "demo")

    target_directory = os.path.join(os.getcwd(), "demo")

    # Call the function to copy the directory
    copy_directory(source_directory, target_directory)

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
                         os.path.join(os.getcwd(), "__template_tests_services_rest"))

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
                         os.path.join(os.getcwd(), "__template_tests_services_graphql"))