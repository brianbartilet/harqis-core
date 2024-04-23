# REST API OpenAPI Test Generation

## Introduction
- Ability to generate out-of-box and run ready tests from a REST API OpenAPI specification from a url or file source.
- Generates the test code using existing core fixtures and utilities which are defined in mustache templates.
- Integrates with OpenAI API to generate test cases from the OpenAPI specification.

## Design
- Use the script `generate.py` to generate the test cases from the OpenAPI specifications in a Python dictionary.
- This dictionary data can be parsed to the test mustache templates to generate the test code.
- Tests are generated into two core processes:
  - **generate test code from OpenAPI** process a URL or file source argument spec to generate the test cases and code from using core fixtures..
  - **update and add test cases using GPT** uploads and analyses the generated files to add more test cases using OpenAI API.
- This demo is still in development and will be updated with more features and functionalities. *bugs*

## Modules
- [`/data`](./data)
  - Contains sample data to upload to GPT
- [`/specs`](./specs)
  - Contains sample OpenAPI specifications to generate test cases
- [`/specs/tasks_api_specs.yaml`](./specs/tasks_api_specs.yaml)
  - Sample input OpenAPI specification to generate test cases
- [`/generate.py`](./generate.py)
  - Main script to generate test code from fixtures and baseline tests *needs additional work*
  - Please see the docstrings and comments in the code for more information and flow.
  - Run command below to script usage and help.
    ```bash
    python generate.py --help
    ```
  - Run with default setup
    ```bash
    python generate.py
    ```
## Generated Files
- [`/generated`](./generated)
  - Contains the generated test code from the OpenAPI specification
  - Mimics the test application structure of [demo REST tests](../example_tests_services_rest/README.md)
- [`/generated/GPT_RESPONSE.md`](./generated/GPT_RESPONSE.md)
  - Store the GPT response from the OpenAI API.

## Run Tests
- Run the service for the mocked openAPI in the Docker compose file.
  ```bash
  cd .. && docker-compose up prism
  ```

- Run the tests using the command below.
  ```bash
  pytest
  ```


