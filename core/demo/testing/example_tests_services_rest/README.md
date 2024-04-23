# REST API Simple Tests

## Introduction
- A simple demo of writing and testing REST API endpoints.
- Contains a basic setup and structure to get started with REST API testing.

## Design
- The [`example_tests_services_rest`](../example_tests_services_rest) represents a target application to be tested.
- This would contain the models, services, resources, configuration and tests for the target application.
- **Please** read docstring and comments in the code for more information.

## Modules
### [`/models`](./models)
- Contains the data models for the tested applications.
- This can be defined from OpenAPI specifications or from existing data models from the application.
### [`/services`](./services)
- Structure to organize the services and corresponding resources of the application.
- This contains reusable service classed to send, receive and process data from the application.
### [`/services/base_service.py`](./services/base_service.py)
- A base service class to be inherited by the services.
- Primary class to integration with core fixtures and utilities.
- Base headers and client setup can be defined here.
### [`/services/posts`](./services/posts)
- Represents a service to organize the resources for the posts endpoint.
### [`/services/posts/post.py`](./services/posts/post.py)
- A service class to interact with the `posts` endpoint.
- Contains the http methods (GET, POST, PATCH, etc.) to interact with the endpoint.
### [`/tests`](./tests)
- Contains the test cases for the services.
- Tests are written in BDD/Cucumber style for readability and maintainability.
- Utilizes `pytest` as the test runner along with its fixtures and utilities.
### [`/tests/post.py`](./tests/post.py)
- Main test file to test the `posts` endpoint.
- Please see the docstrings and comments in the code for more information.
### [`/config.py`](./config.py)
- Contains the configuration for the tests, loads from the configuration [`sample_config.yaml`](../../sample_config.yaml).
- Please see the docstrings and comments in the code for more information.

## Run Tests
- To run the tests, execute the following command:
  *win*
  ```bash
  ..\..\scripts\set_env.bat && pytest tests
  ```
  *linux*
  ```bash
  sh ..\..\scripts\set_env.sh && pytest tests
  ```