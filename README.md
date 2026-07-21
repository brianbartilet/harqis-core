# HARQIS: Heuristic Automation for Resilient, Queryable Integration Systems

## Introduction

- **HARQIS-core** is the reusable foundation for HARQIS: configuration, service fixtures, browser automation, code generation, Celery execution, logging, and testing utilities.
- The deployed automation and second-brain platform lives in [**harqis-work**](https://github.com/brianbartilet/harqis-work), which composes these primitives into app integrations, workflows, MCP tools, and AI agents.
- AI-assisted features have moved to **harqis-work** and are model-neutral; available models, tools, and invocation depend on the active agent harness.

## Key Features

### Automation Swiss Army Knife

- **Generic Automation**: Provides comprehensive support for both general automation tasks and testing.
- **Ease of Use**: Offers reusable fixtures for web services, browser automation, configuration, and workflow execution.
- **Adaptability**: Easily adjusts to dynamic environments, automation strategies, and evolving requirements.
- **Resilient, Queryable Integrations**: Combines reusable service fixtures, configuration, logging, scheduled execution, and test utilities so integrated systems can be operated and inspected consistently.

#### Use Cases
- Facilitates the creation of a generic test automation framework.
- Supports end-to-end, integration, functional and non-functional testing.
- Provide reporting and analytics.
- Provide utility decorators to apply testing principles and techniques.

### AI-Assisted Development *(moved to harqis-work)*
> **Note:** The former OpenAI GPT integration (`core/apps/gpt`) has been removed. AI-assisted development is maintained in [**harqis-work**](https://github.com/brianbartilet/harqis-work), where repository skills can guide Claude, OpenAI models, and other capable reasoning models when supported by their harness.

- **HARQIS-core boundary**: Keeps deterministic fixtures, generators, configuration, and execution primitives independent of any model provider.
- **HARQIS-work ownership**: Provides the agent integrations and reusable skills that apply those primitives to development and operations.

#### Use Cases
- Automates the generation of test code based on existing fixtures and templates.
- Offers code analysis and suggestions for testing techniques.
- Generates test code by analyzing static specifications or schemas (e.g. *OpenAPI*, *GraphQL*, *WSDL*) from available fixtures and templates.

### Cross-Application Integration and Workflow Orchestration
- **Create Robots**: Provides RPA-like capabilities to automate any workflow from integrated applications.
- **Celery Orchestration**: Provides code-based task scheduling and execution primitives for composing application workflows.

#### Use Cases
- Publish workflow tasks as events that can be consumed for execution.
- Support e2e testing and task automation.

## Features Inventory
Please refer here for the complete map of the [HARQIS Features](core/docs/FEATURES.md).

## Demo Project
- Please refer to [harqis-demo-generic-framework](https://github.com/brianbartilet/harqis-demo-generic-framework) for a sample application of **HARQIS-core**.
- The demo project can be used as a template for creating new projects and providing basic operations of fixtures and templates.
- See the [README.md](https://github.com/brianbartilet/harqis-demo-generic-framework/blob/main/README.md)

## Contact
For questions or feedback, please contact [brian.bartilet@gmail.com](mailto:brian.bartilet@gmail.com).


## Contributing

We welcome contributions! If you have ideas for new features or improvements, please submit a pull request or open an issue.

Please refer here to this [project](https://github.com/users/brianbartilet/projects/1) containing features completed or to be developed.

## Getting Started

To get started with **HARQIS-core**, follow these steps:

**Setup and Installation**:
   - Runs on Python 3.12
   - Clone the repository
      ```sh
      git clone https://github.com/brianbartilet/harqis-core.git
      ```
   - Set up and activate the virtual environment
     *windows*
     ```powershell
      python -m venv venv
      .\venv\Scripts\Activate.ps1
     ```
     *linux*
     ```sh
      python -m venv venv
      source venv/bin/activate
      ```
   - Install the package and its development dependencies
      ```sh
      python -m pip install --upgrade pip
      pip install -e ".[dev]"
      ```

**Configuration**:
   - A configuration requirement is needed to run the apps integrated into the framework. Replace or update the `apps_config.yaml` file in the root directory and add the following:
      ```yaml
      CELERY_TASKS:
        application_name: 'workflow-harqis'
        broker: 'your_broker_url'
      ```
   > **Note:** AI integrations are managed in **harqis-work** and are not configured by **HARQIS-core**.
   - Supporting services are defined in the root [`docker-compose.yaml`](docker-compose.yaml).

**Run the Test Suite**:
- Execute the suite using the following command:
   ```sh
   cd core
   pytest
   ```
- Most tests are isolated, but development-mode resource-download and browser-driver checks use live network services and installed browsers. A missing browser, driver host, or upstream fixture can fail those environment-dependent checks.

**Docker**:
- Alternatively, you may test the package from the provided `Dockerfile`, by executing the following commands:
   ```sh
   docker build . -t harqis-core --target base
   docker run -v app_volume:/app/data harqis-core
   ```
- Enable dependencies from Docker compose
  ```sh
  docker compose up
  ```

**Package Management**:
- To build the package, execute the following command:
   ```sh
   python -m build
   ```
 - Runtime dependencies are bounded direct requirements in `pyproject.toml`.
   `core/requirements.txt` is retained only as a legacy environment snapshot
   and is not published as package metadata.


## License

**HARQIS-core** is distributed under the [MIT License](LICENSE).


