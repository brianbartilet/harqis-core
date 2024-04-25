# Cucumber BDD with Selenium Webdriver

## Introduction
- Create automated tests from features as supported by behave and selenium webdriver.
- Utilize the Page Object Model to create a more maintainable test suites.

## Design
- Utilizes two core fixtures to set up a page model and a webdriver instance.
  - `BaseFixtureWebDriver` - Sets up a webdriver instance.
  - `BaseFixturePageModel` - Sets up a page model instance.
- Utilizes a hooks manager for behave hooks to make procedures more maintainable.

## Modules
- `/features` - Contains the feature files.
- `/features/status_codes` - A sample module directory to contain feature files.
- `/features/steps` - Contains the step definitions.
- `/features/steps/common.py` - Contains common step definitions across features.
- `/features/steps/status_codes.py` - Examples step definitions for the status codes feature.
- `/features/environment.py` - Contains the behave environment setup and hooks, utilizes a hooks manager.
- `/references` - Contains page model references and other data related definitions.
- `/references/data` - Contains data related definitions.
- `/references/hooks` - Oganizes hooks for the behave environment.
- `/references/pages` - Contains page model definitions.
- `/references/base_page.py` - Creates a base page model class for target application.

## Run Tests
- Run all tests using the following command:
  *windows*
  ```bash
  ..\..\scripts\set_env.bat && behave
  ```
  *linux*
  ```bash
  sh ..\..\scripts\set_env.sh && behave
  ```