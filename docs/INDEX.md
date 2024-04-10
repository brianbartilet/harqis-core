# HARQIS Core Inventory

### Status
| :triangular_ruler: *Planned* | :construction: *In Progress* | :white_check_mark: *Completed* | :pause_button: *On Hold* |
|------------------------------|------------------------------|--------------------------------|--------------------------|


## Core Automation and Testing
### Unit Testing
#### :white_check_mark: pytest
- [pytest](https://docs.pytest.org/en/stable/) is a testing framework that makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.
- this framework utilizes `pytest` fixtures and related plugins to support various testing scenarios.

### Web Services Testing
- utilizes the [requests](https://requests.readthedocs.io/en/latest/) library for sending and receiving HTTP requests.
- provided reusable fixtures for testing and contracts for scalable and maintainable tests.
#### :white_check_mark: REST
- provides reusable fixtures for testing REST APIs.
- support for [OpenAPI](https://spec.openapis.org/oas/latest.html) specifications and [Swagger](https://swagger.io/specification/).
- support for mocking REST APIs using [Stoplight Prism](https://docs.stoplight.io/docs/prism/f51bcc80a02db-installation).
#### :white_check_mark: GraphQL
- provides reusable fixtures for testing [GraphQL](https://graphql.org/) queries and mutations.
#### :white_check_mark: SOAP
- provides reusable fixtures for testing [SOAP XML](https://www.w3schools.com/xml/xml_soap.asp) services.
#### :triangular_ruler: gRPC
- support in progress for [gRPC](https://grpc.io/) services.
#### :triangular_ruler: Contract Testing

### Frontend Testing
#### :white_check_mark: Selenium
#### :triangular_ruler: Beautiful Soup
#### :triangular_ruler: Appium
#### :construction: BDD behave

### Test Automation Fixtures
#### :white_check_mark: REST API Testing
#### :white_check_mark: GraphQL Testing
#### :construction: Page Object Model Testing
#### :construction: Behave Hooks management
#### :white_check_mark: Configuration Management

### Non-Functional Testing
#### :triangular_ruler: Locust

### Embedded Systems and IoT
#### :triangular_ruler: MQTT

### Code Generation
#### :white_check_mark: Mustache Support
#### :white_check_mark: REST API
#### :construction: GraphQL
#### :construction: Page Object Model Testing

### Mocking
#### :white_check_mark: OpenAPI with Docker Prism

### Containerization
#### :white_check_mark: Docker and Docker Compose

### Package Management
#### :white_check_mark: pip and setup.py

## Tasks Automation
#### :white_check_mark: Task Scheduling Using Celery
- utilizes [RabbitMQ](https://www.rabbitmq.com/docs) as a broker
- refer to [README.md](../core/apps/sprout/README.md) for complete documentation

#### :triangular_ruler: Tasks Creation Using Flower

## Reporting and Analytics
#### :triangular_ruler: Allure Reporting

## Observability and Monitoring
#### :triangular_ruler: Elastic Stack

## Integrations
#### :white_check_mark: OpenAI API

## Utilities
### Communication
#### :triangular_ruler: Web Sockets
#### :white_check_mark: ssh
### Data
#### :white_check_mark: LINQ Python Utility
- simplified list comprehension using LINQ-like syntax
#### :triangular_ruler: Faker Utilities