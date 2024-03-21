# HARQIS: Heuristic Automation for a Reliable Quality Integration System

## Introduction

- **HARQIS** (Heuristic Automation for a Reliable Quality Integration System) is a versatile automation platform designed to facilitate a wide range of automation tasks across various domains.
- **GPT** integrated functionalities, leverages the **OpenAI API** to assist with code generation and analysis.
- Provides fixtures, utilities, and templates for implementing automation for various applications and systems. It enables the creation of automated workflows for testing, cross application integration, and more, adapting to both small and large-scale projects with ease.

## Key Features

### Automation Swiss Army Knife

- **Generic Automation**: Provides comprehensive support for both general automation tasks and testing.
- **Ease of Use**: Offers automation fixtures for frontend, backend, embedded systems, and IoT applications.
- **Adaptability**: Easily adjusts to dynamic environments and evolving requirements.
- **Quality Integration System**: Ensures testing standards and optimal performance of integrated components and systems.

#### Use Cases
- Facilitates the creation of a generic test automation framework.
- Supports end-to-end, integration, and functional testing.
- Provide reporting and analytics.
- Provide utility decorators to apply testing principles and techniques.

### GPT Assisted Development
- **Development Assistant**: Utilizes the *OpenAI API* to generate test code, analyze fixtures, and apply testing techniques.
- **OpenAI Integration**: Directly integrates with the *OpenAI API* to create scripts and perform other useful tasks.

#### Use Cases
- Automates the generation of test code based on existing fixtures and templates.
- Offers code analysis and suggestions for testing techniques.
- Generates test code from analyzing static specifications or schemas (e.g. *OpenAPI*, *GraphQL*, *WSDL*) from available fixtures and templates.

### Cross Application Integration and Workflow Builder
- **Create Robots**: Provides RPA-like capabilities to automate any workflow from integrated applications.
- **Workflow Builder**: Features a workflow builder (akin to *Zapier* or *IFTTT*) for code-based, fully controllable application data and task scheduling.

#### Use Cases
- Publish workflows tasks as events that can be consumed for execution.
- Support e2e testing and task automation.

## Demo Project
- Please refer here [harqis-demo-generic-framework](https://github.com/brianbartilet/harqis-demo-generic-framework) for an sample application of **HARQIS-core**.
- The demo project can be used as a template for creating new projects and provide basic operations of fixtures and templates.
- See the [README.md](https://github.com/brianbartilet/harqis-demo-generic-framework/blob/main/README.md)

## Contact

For questions or feedback, please contact [brian.bartilet@gmail.com](mailto:brian.bartilet@gmail.com).


## Contributing

We welcome contributions! If you have ideas for new features or improvements, please submit a pull request or open an issue.

Please refer here to this [project](https://github.com/users/brianbartilet/projects/1) containing features completed or to be developed.
## Getting Started

To get started with **HARQIS-core**, follow these steps:

**Setup and Installation**:
   - Runs on Python 3.10 or greater.
   - Clone the repository
      ```sh
      git https://github.com/brianbartilet/harqis-core.git
      ```
   - Set up and activate virtual environment
      ```sh
      python -m venv venv
      source venv/bin/activate
      ```
   - Install the required packages using the requirements file
      ```sh
      pip install --upgrade pip
      pip install -r requirements.txt
      ```

**Configuration**:
   - A configuration requirement is needed to run the application. Create a `apps_config.yaml` file in the root directory and add the following:
      ```yaml
      CELERY_TASKS:
        application_name: 'workflow-harqis'
        broker: 'your_broker_url'
      HARQIS_GPT:
        client: 'rest'
        parameters:
          base_url: 'https://api.openai.com/v1'
          response_encoding: 'utf-8'
          verify: False
          timeout: 60
          stream: True
      app_data:
        api_key: 'your_openai_api_key'
        model: 'your_target_assistant_mode'
        max_tokens: 500
      ```
**Run Unit Tests**:
- Execute all tests using the following command:
   ```sh
   pytest
   ```
**Docker**:
- For local testing please execute `docker-compose up` to run the application dependencies.
- Alternatively you may test the package from provided `Dockerfile`, by executing the following commands:
   ```sh
   docker build . -t harqis-core
   docker run harqis-core
   ```

**Test Package Build**:
- To build the package, execute the following command:
   ```sh
   python setup.py sdist bdist_wheel
   ```

## License

**HARQIS-core** is distributed under the [MIT License](LICENSE).


