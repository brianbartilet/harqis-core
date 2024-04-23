# REST API Simplified Tests

## Introduction
- a simple demo of writing and testing REST API endpoints.
- contains a basic setup and structure to get started with REST API testing.

## Design
- the [`example_tests_services_rest`](../example_tests_services_rest) represents a target application to be tested.
- this would contain the models, services, resources, configuration and tests for the target application.
- **please** read docstring and comments in the code for more information.

## Modules
### [`/models`](./models)
- contains the data models for the tested applications.
- this can be defined from OpenAPI specifications or from existing data models from the application.
### [`/services`](./services)
- structure to organize the services and corresponding resources of the application.
- this contains reusable service classed to send, receive and process data from the application.
### [`/services/base_service.py`](./services/base_service.py)
- a base service class to be inherited by the services.
- primary class to integration with core fixtures and utilities.
- base headers and client setup can be defined here.
### [`/services/posts`](./services/posts)
- represents a service to organize the resources for the posts endpoint.
### [`/services/posts/post.py`](./services/posts/post.py)
- a service class to interact with the `posts` endpoint.
- contains the http methods (GET, POST, PATCH, etc.) to interact with the endpoint.
### [`/tests`](./tests)
- contains the test cases for the services.
- tests are written in BDD/Cucumber style for readability and maintainability.
- utilizes `pytest` as the test runner along with its fixtures and utilities.
### [`/tests/post.py`](./tests/post.py)
- main test file to test the `posts` endpoint.
- please see the docstrings and comments in the code for more information.
### [`/config.py`](./config.py)
- contains the configuration for the tests, loads from the configuration [`sample_config.yaml`](../../sample_config.yaml).
- please see the docstrings and comments in the code for more information.

## Run Tests
- to run the tests, execute the following command:
```bash
pytest tests/*
```