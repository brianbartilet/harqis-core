# HARQIS Features Inventory

### Status
| :triangular_ruler: Planned | :construction: In Progress | :white_check_mark: Completed | :pause_button: On Hold | :no_entry: Deprecated |
|----------------------------|----------------------------|------------------------------|------------------------|-----------------------|


## Core Automation and Testing
### Unit Testing
#### :white_check_mark: pytest
![pytest](https://img.shields.io/badge/pytest-8.0.2-blue)
- [pytest](https://docs.pytest.org/en/stable/) is a testing framework that makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.
- this framework utilizes `pytest` fixtures and related plugins to support various testing scenarios.

### Web Services Testing
![requests](https://img.shields.io/badge/requests-2.31.0-blue)
- utilizes primarily the [requests](https://requests.readthedocs.io/en/latest/) library for sending and receiving HTTP requests.
- provide reusable fixtures for testing and contracts for scalable and maintainable tests.

| Service                              | Description                                                                                                                     | Dependencies                                               |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| :white_check_mark: REST API          | provide reusable fixtures for testing REST APIs supporting [OpenAPI](https://spec.openapis.org/oas/latest.html) specifications. |                                                            |
| :white_check_mark: GraphQL           | provide reusable fixtures for testing [GraphQL](https://graphql.org/) queries and mutations.                                    |                                                            |
| :triangular_ruler: gRPC              | support in progress for [gRPC](https://grpc.io/) services.                                                                      | ![grpcio](https://img.shields.io/badge/grpcio-1.62.0-blue) |
| :white_check_mark: SOAP              | provides reusable fixtures for testing [SOAP XML](https://www.w3schools.com/xml/xml_soap.asp) services.                         |                                                            |
| :triangular_ruler: Contract Testing  | development in progress to provide [contract testing](https://docs.pact.io/) using `pact-python`.                               |

### Frontend Testing
- utilizes web drivers and related utilities to perform mobile, web and/or desktop frontend automated testing.
- provide reusable fixtures for testing and contracts for scalable and maintainable tests.

| Service                           | Description                                                                                                                                                                                                                           | Dependencies                                                               |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| :white_check_mark: Selenium       | provide reusable fixture for testing web applications utilizing [web drivers](https://www.selenium.dev/documentation/webdriver/) and allow support for Page Object Model testing.                                                     | ![selenium](https://img.shields.io/badge/selenium-4.18.0-blue)             |
| :triangular_ruler: Beautiful Soup | provide reusable fixture for scraping web pages using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and organize scraped data into structured data for further processing utilizing the Page Object Model. | ![beautifulsoup4](https://img.shields.io/badge/beautifulsoup4-4.12.0-blue) |
| :triangular_ruler: Appium         | provide reusable fixture utilizing [Appium](http://appium.io/) client for mobile application testing.                                                                                                                                 |                                                                            |
| :triangular_ruler: Playwright     | provide reusable fixture utilizing [Playwright](https://playwright.dev/) for web application testing.                                                                                                                                 |                                                                            |
| :construction: BDD behave         | Utilities to enhance BBD test development using [behave](https://behave.readthedocs.io/en/stable/).                                                                                                                                   |                                                                            |

### Test Automation Fixtures
- please see web services [README.md](../core/web/services/README.md) documentation for more details of provided test fixtures.
- for examples and how-to-use please refer to the demo docs guide [INDEX.md](../core/demo/docs/INDEX.md)

| Fixture                                     | Description                                                  |
|---------------------------------------------|--------------------------------------------------------------|
| :white_check_mark: REST API                 | fixture for testing REST APIs                                |
| :white_check_mark: GraphQL                  | fixture for testing GraphQL APIs                             |
| :construction: Page Object Model Testing    | fixture for testing web applications using Page Object Model |
| :construction: Behave Hooks management      | fixture for managing behave hooks                            |
| :white_check_mark: Configuration Management | fixture for managing configuration files                     |

### Non-Functional Testing
#### :triangular_ruler: Locust
- support in progress for [Locust](https://locust.io/) for load and performance testing.

### Embedded Systems and IoT
#### :triangular_ruler: MQTT
- support in progress for [MQTT](https://mqtt.org/) protocol for IoT testing.

### Code Generation
#### :white_check_mark: Mustache Support
![pystache](https://img.shields.io/badge/pystache-0.6.5-blue)
- support code generation from fixtures using [Mustache](https://mustache.github.io/) templates.
- please see the [README.md](../core/codegen/README.md) for more implementation details.

| Generation                               | Description                                                 |
|------------------------------------------|-------------------------------------------------------------|
| :white_check_mark: REST API              | generates baseline tests from fixtures given a OpenAPI spec |
| :construction: GraphQL                   | generates baseline tests from schemas                       |
| :construction: Page Object Model Testing | generates boiler Page Object Model from a definition        |


### Mocking
- modules to provide mocking services for testing and development.
- refer to this [README.md](../core/web/README.md) for additional information

| Mocking Service                                | Description                              |
|------------------------------------------------|------------------------------------------|
| :white_check_mark: OpenAPI Specification Mocks | Mocking REST APIs using Stoplight Prism  |

### Tasks and Workflows Automation
#### :white_check_mark: Task Scheduling Using Celery
- utilizes [RabbitMQ](https://www.rabbitmq.com/docs) as a broker
- refer to [README.md](../core/apps/sprout/README.md) for complete documentation
#### :triangular_ruler: Tasks Creation Using Flower

## Reporting and Analytics
#### :triangular_ruler: Allure Reporting
- provide reusable fixture for generating [Allure](https://docs.qameta.io/allure/) reports across different tested applications.

## Observability and Monitoring
#### :triangular_ruler: Elastic Stack
- support in progress for [Elastic Stack](https://www.elastic.co/elastic-stack) for observability and monitoring for testing results and quality metrics.
- monitor and analyze logs, metrics, and other data from various testing sources.
- sample use cases: performance monitoring, bug density and test coverage analysis.

## Integrations
#### :white_check_mark: OpenAI API
- support for [OpenAI](https://platform.openai.com/overview) API for AI-powered testing and automation.

## Utilities
### Communication
#### :triangular_ruler: Web Sockets
- support in progress for [Web Sockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) for real-time communication.
#### :white_check_mark: ssh
- utilities for managing ssh connections and executing commands on remote servers.

### Data Helpers
#### :white_check_mark: LINQ Python Utility
- simplified list comprehension using LINQ-like syntax
#### :triangular_ruler: Faker Utilities
- generate fake data for testing and development.
- support in progress for [Faker](https://faker.readthedocs.io/en/master/) utilities.

### Deployment and Containerization
#### :white_check_mark: Docker and Docker Compose
- all fixtures and utilities are containerized for easy deployment and scaling.
- please see documentation here [DEPLOYMENT.md](features/DEPLOYMENT.md) for more details.
#### :white_check_mark: HARQIS Package Management
- please refer to the [PACKAGE.md](features/PACKAGE.md) for more details on managing packages and dependencies for this project.

## Contact
For suggestions, questions or feedback, please contact [brian.bartilet@gmail.com](mailto:brian.bartilet@gmail.com).
