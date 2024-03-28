FEATURES
- add only graphql files

TODO:

- add pickling correct for response
- add get error message from response


Steps
1. Setup Config
2. Intialize the client


# GPT Instructions
### Core Instruction
From the zip files containing a sample structure of references and tests along with the provided package library, generate test code and structure from the provided OpenAPI specifications file.

### Uploaded Files
- `core.web.services.zip` - web services library that is utilized by the template below
- `___tpl_tests_services_rest.zip` - template implementation along with the tests of the `core.web.services.zip`

### Files Directories
Please see the explanation below for the contents of the uploaded files.

#### ___tpl_tests_services_rest.zip
- `/___tpl_tests_services_rest/dto` - folder to contain data transfer objects that can be provided from an open API specification
- `/___tpl_tests_services_rest/dto/user.py` - sample data transfer object that inherits from `JsonObject` defined in the `core.web.services` package
- `/___tpl_tests_services_rest/dto/payload.py`- same as above
- `/___tpl_tests_services_rest/services` - serves as a reference directory to store implementation of fixtures from `core.web.services`
- `/___tpl_tests_services_rest/services/base_service.py` - base class for implementation of `BaseFixtureServiceRest` from the package `core.web.services` under `/fixtures`
- `/___tpl_tests_services_rest/services/posts` - a directory for organizing REST services usually a resource name
- `/___tpl_tests_services_rest/services/posts/post.py` - a reusable class for sending requests to a REST resource that can be used for testing and other integrations
- `/___tpl_tests_services_rest/tests/integration` - directory to organize integration tests and API chaining scenarios
- `/___tpl_tests_services_rest/tests/sanity` - basic tests to test functionality and negative tests
- `/___tpl_tests_services_rest/tests/sanity/post.py` - tests written in `pytest`, this would be the primary output that we would want to generate.

#### core.web.services.zip
- `/services/core` - core packages and code to perform web services testing and integration.
- `/services/core/clients` - web clients
- `/services/core/config` - classes to standardize configuration structure across web services
- `/services/core/constants` - constants related to web services
- `/services/core/contract` - interfaces to build implementation for web services dependencies
- `/services/core/request_builder` - create a chainable way for building web requests
- `/services/core/json.py` - collection JSON helpers
- `/services/core/request.py` - request class to store web request information
- `/services/core/response.py` - response class to store web response information
- `/services/core/tests` - unit tests for testing the library and also is the baseline structure of `___tpl_tests_services_rest.zip`
- `/services/core/fixtures` - core fixtures to be used to build service classes and is a composition class of dependencies included for the whole package.  This is used and applied depending on the context of the web service to be used.
- `/services/core/fixtures/rest.py` - the primary fixture that is used to create REST testing implementation and organization of services this is reference `___tpl_tests_services_rest/services/base_service.py`

#### tasks_api_specs.yaml
- A YAML file defining OpenAPI specifications and the primary entry criteria of the task.
- The goal is to generate code and structure from `___tpl_tests_services_rest` as a baseline.


 ### Additional Instructions
 - The exit criteria is to generate code and explanation of code using docstrings
 - Test cases should cover sanity tests to test endpoints and some negative testing derived from boundary value analysis and equivalence partitioning.