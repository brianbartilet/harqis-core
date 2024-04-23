# Simple Tests for GraphQL Services

## Introduction
- A simple demo of writing and testing GraphQL services utilizing core fixtures.
- Contains a basic setup and structure to get started with GraphQL services testing.

## Design
- The [`example_tests_services_graphql`](../example_tests_services_graphql) represents a GraphQL target service to be tested.
- Supports backend for a frontend (BFF) service or a standalone GraphQL service.
- This would contain the requests, models, configuration and tests for the target application.
- Requests are organized in `.gql` files to be used in the tests for organization, readability and simplicity.
- These requests are then processed with the necessary parameters and variables to be sent to the GraphQL endpoint.
- **Please** read docstring and comments in the code for more information.
- Common configuration processing is located in the [`config.py`](./config.py) file.
- Data handling and processing still under development.

## Mutations Module
### [`/mutations`](./mutations)
- Organize the GraphQL mutation requests for the tested applications.
### [`/mutations/save_media_list_entry`](./mutations/save_media_list_entry)
- A sample mutation to save a media list entry.
- This directory organizes the mutations request using a `.gql` template file along with the models and requests

## Queries Module
### [`/queries`](./queries)
- Organize the GraphQL query requests for the tested applications.
### [`/queries/get_media`](./queries/get_media)
- A sample query to get media information.
- This directory organizes the queries request using a `.gql` template file along with the models and requests

## Tests Module
- Tests are written in BDD/Cucumber style for readability and maintainability.
- Please see the docstrings and comments in the code for more information.
- Utilizes `pytest` as the test runner along with its fixtures and utilities.
### [`/tests/mutations`](./tests/mutations)
- Organize the tests for the GraphQL mutations.
### [`/tests/queries`](./tests/queries)
- Organize the tests for the GraphQL queries.

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

## References
- Core [GraphQL](https://graphql.org/learn/) documentation