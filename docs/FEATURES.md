# HARQIS Core Features Inventory
- Provided below is a comprehensive list of features and utilities available in **HARQIS-core**
- This would help users understand the capabilities and functionalities and how it can be utilized for various automation and testing tasks.
- Please refer to the [README.md](https://github.com/brianbartilet/harqis-core/blob/main/README.md#use-cases) for more information on the framework and its use cases.
#### Development Status
| :bulb: Planned | :arrow_forward: In Progress | :white_check_mark: Completed | :pause_button: On Hold | :no_entry: Deprecated |
|----------------|-----------------------------|------------------------------|------------------------|-----------------------|


## Core Automation and Testing
### Unit Testing
#### :white_check_mark: pytest
- [**pytest**](https://docs.pytest.org/en/stable/) is a testing framework that makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.
- This framework utilizes `pytest` fixtures and related plugins to support various testing scenarios.

### Web Services Automation
- Utilizes primarily the [**requests**](https://requests.readthedocs.io/en/latest/) library for sending and receiving HTTP requests.
- Provides reusable fixtures for testing and contracts for scalable and maintainable tests.

| Service                         | Description                                                                                                                         | Dependencies                                                                                                                  |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| :white_check_mark: **REST API** | provide reusable fixtures for testing REST APIs supporting [**OpenAPI**](https://spec.openapis.org/oas/latest.html) specifications. | ![pytest](https://img.shields.io/badge/pytest-8.0.2-blue)</br>![requests](https://img.shields.io/badge/requests-2.31.0-blue)  |
| :white_check_mark: **GraphQL**  | provide reusable fixtures for testing [**GraphQL**](https://graphql.org/) queries and mutations.                                    | ![pytest](https://img.shields.io/badge/pytest-8.0.2-blue)</br>![requests](https://img.shields.io/badge/requests-2.31.0-blue)  |
| :arrow_forward: **gRPC**        | support in progress for [**gRPC**](https://grpc.io/) services.                                                                      | ![pytest](https://img.shields.io/badge/pytest-8.0.2-blue)</br>![grpcio](https://img.shields.io/badge/grpcio-1.62.0-blue)      |
| :arrow_forward: **SOAP XML**    | provides reusable fixtures for testing [**SOAP XML**](https://www.w3schools.com/xml/xml_soap.asp) services.                         | ![pytest](https://img.shields.io/badge/pytest-8.0.2-blue)</br>![requests](https://img.shields.io/badge/requests-2.31.0-blue)  |
| :bulb: **Contract Testing**     | development in progress to provide [**contract testing**](https://docs.pact.io/) using `pact-python`.                               |                                                                                                                               |

### Frontend Automation
- Utilizes web drivers and related utilities to perform mobile, web and/or desktop frontend automated testing.
- Provide reusable fixtures for testing and contracts for scalable and maintainable tests.

| Service                         | Description                                                                                                                                                                                                                               | Dependencies                                                               |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| :white_check_mark: **Selenium** | provide reusable fixture for testing web applications utilizing the [**web driver**](https://www.selenium.dev/documentation/webdriver/) and allow support for Page Object Model testing.                                                  | ![selenium](https://img.shields.io/badge/selenium-4.18.0-blue)             |
| :bulb: **Beautiful Soup**       | provide reusable fixture for scraping web pages using [**Beautiful Soup**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and organize scraped data into structured data for further processing utilizing the Page Object Model. | ![beautifulsoup4](https://img.shields.io/badge/beautifulsoup4-4.12.0-blue) |
| :bulb: **Appium**               | provide reusable fixture utilizing [**Appium**](http://appium.io/) client for mobile application testing.                                                                                                                                 |                                                                            |
| :bulb: **Playwright**           | provide reusable fixture utilizing [**Playwright**](https://playwright.dev/) for web application testing.                                                                                                                                 |                                                                            |
| :arrow_forward: **BDD**         | Utilities to enhance BDD test development using [**behave**](https://behave.readthedocs.io/en/stable/).                                                                                                                                   |                                                                            |

### Testing Fixtures
- Please see fixtures [README.md](https://github.com/brianbartilet/harqis-core/blob/main/core/web/README.md#fixtures) documentation for more details of provided test fixtures.
- For examples and how-to-use please refer to the demo docs guide [DEMO.md](DEMO.md)

| Fixture                                         | Description                                                  |
|-------------------------------------------------|--------------------------------------------------------------|
| :white_check_mark: **REST API**                 | fixture for testing REST APIs                                |
| :white_check_mark: **GraphQL**                  | fixture for testing GraphQL APIs                             |
| :arrow_forward: **Page Object Model**           | fixture for testing web applications using Page Object Model |
| :arrow_forward: **Behave Hooks Management**     | fixture for managing behave hooks                            |
| :white_check_mark: **Configuration Management** | fixture for managing configuration files                     |

### Non-Functional Testing
#### :bulb: Locust
- Support in progress for [**Locust**](https://locust.io/) for load and performance testing.

### Embedded Systems and IoT
#### :bulb: MQTT
- Support in progress for [**MQTT**](https://mqtt.org/) protocol for IoT testing.

### Test Code Generation
#### :white_check_mark: Python Mustache Code Generator
![pystache](https://img.shields.io/badge/pystache-0.6.5-blue)
- Support code generation from supported testing [fixtures](#testing-fixtures) using [**Mustache**](https://mustache.github.io/) templates.
- Please see the [README.md](https://github.com/brianbartilet/harqis-core/blob/main/core/codegen/README.md) for more implementation details.

| Generation                            | Description                                           |
|---------------------------------------|-------------------------------------------------------|
| :white_check_mark: **REST API**       | generates baseline tests from a OpenAPI spec          |
| :arrow_forward: **GraphQL**           | generates baseline tests from a GraphQL introspection |
| :arrow_forward: **Page Object Model** | generates page object model from a definition         |

### Mocking
- Modules to provide mocking services for testing and development.
- Refer to this [README.md](https://github.com/brianbartilet/harqis-core/blob/main/core/web/README.md#mocking) for additional information

| Service                                | Description                                                 |
|----------------------------------------|-------------------------------------------------------------|
| :white_check_mark: **OpenAPI Mocking** | Mocking REST APIs using Stoplight Prism from a OpenAPI spec |

### Tasks And Workflows Automation
#### :white_check_mark: Task Scheduling via Python [**celery**](https://docs.celeryq.dev/en/v5.3.6/getting-started/introduction.html)
![celery](https://img.shields.io/badge/celery-5.3.6-blue)
- Utilizes [**RabbitMQ**](https://www.rabbitmq.com/docs) as a broker
- Monitor and manage tasks using [**flower**](https://flower.readthedocs.io/en/latest/)
- Refer to this [README.md](https://github.com/brianbartilet/harqis-core/blob/main/core/apps/sprout/README.md) for complete documentation and how to use.


## Reporting and Analytics
#### :bulb: Allure Reporting
- Provide reusable fixture for generating [**Allure**](https://docs.qameta.io/allure/) reports across different tested applications.

## Observability and Monitoring
#### :bulb: Elastic Stack
- Support in progress for [**Elastic Stack**](https://www.elastic.co/elastic-stack) for observability and monitoring for testing results and quality metrics.
- Monitor and analyze logs, metrics, and other data from various testing sources.
- Sample use cases: performance monitoring, bug density and test coverage analysis.

## Integrations
#### :white_check_mark: OpenAI API
- Support for [**OpenAI**](https://platform.openai.com/overview) API for AI-powered testing and automation.

## Utilities
### Communication
#### :white_check_mark: ssh
- Utilities for managing ssh connections and executing commands on remote servers.

### Data Helpers
#### :white_check_mark: LINQ Python Utility
- Simplified list comprehension using [**LINQ**](https://learn.microsoft.com/en-us/dotnet/csharp/linq/) syntax
#### :bulb: Faker Utilities
- Generate fake data for testing and development.
- Support in progress for [**Faker**](https://faker.readthedocs.io/en/master/) utilities.

### Deployment and Containerization
#### :white_check_mark: Docker and Docker Compose
- All fixtures and utilities are containerized for easy deployment and scaling.
- Please see documentation here [DEPLOYMENT.md](features/DEPLOYMENT.md) for more details.
#### :white_check_mark: HARQIS Package Management
- Please refer to the [PACKAGE.md](features/PACKAGE.md) for more details on managing packages and dependencies for this project.

## Contributing
For suggestions, questions or feedback, please contact [brian.bartilet@gmail.com](mailto:brian.bartilet@gmail.com).
