# Instructions
Create a Python data dictionary that contains integration and negative test cases from given mustache templates and fixtures.  Generate it in a text file for download.

### Context:
- Use the `mustache\templates\test.mustache` template as reference to generate the test cases in form of a Python dictionary.
- Use the files from `generated\services` for the request to generate the test cases.
- Use the test model `mustache\models\test.py` from `mustache\models`.
- Complete `@pytest.mark.{{test_suite_name}}` pytest decorator for test suite e.g. `@pytest.mark.integration` and `@pytest.mark.negative`.
- Complete `@pytest.mark.{{test_technique}}` pytest decorator for test techniques e.g. `@pytest.mark.boundary` and `@pytest.mark.equivalence`.
- Provide explanation of code using Google style docstrings using the `{{description}}`.
- Set the `{{#not_implemented}}` flag always to `True` for future review and implementation.

#### data.zip
- `data/test_cases.json` - a sample output file that you can use as reference for the expected output.
#### specs.zip
- `specs/tasks_api_specs.yaml` - A YAML file defining OpenAPI specifications and the primary entry criteria of the task.
- The goal is to generate additional test code, replicated structure from `generated.zip` as a baseline.

#### generated.zip
- `/models` - folder to contain data transfer objects that can be provided from an open API schema
- `/services` - serves as a reference directory to store implementation of fixtures from an external library defined
- `/tests` - tests written in `pytest`, this would be the primary output that we would want to generate with GPT
- `base_service.py` - a base class to implement the service class fixture
- `config.py` - configuration script to initialize the test environment
- `config.yaml` - configuration file to store the test environment

#### mustache.zip
- `/models` - models used to organize data from the API schema to the templates
- `/templates` - mustache templates used to generate code for the tests
- `/generate.py` - script to generate code from the templates and models using OpenAPI specifications
- `/transform.py` - script to transform the OpenAPI data to the desired output

