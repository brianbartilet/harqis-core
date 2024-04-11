# Core Web Documentation
- This document outlines the core implementations to support test automation across application layers for any application under test.
- Please refer to docstrings in the code for more information.

## Modules
### core.web.browser
- `/browser` - contains the core implementations to test various web applications.
### core.web.mobile
- `/mobile` - contains the core implementations to test various mobile applications.
### core.web.services
- `/services` - contains the core implementations to test various web services.
### core.web.mocks
- `/mocks` - contains the core implementations to mock various web services.

## Fixtures
- Fixtures are reusable components that can be used to set up the state of the system under test.
- Please see the currently supported fixtures below and their corresponding demo documentation.

| Fixture                         | Description               | How to Use                                    |
|---------------------------------|---------------------------|-----------------------------------------------|
| `/services/fixtures/rest.py`    | Test fixture for REST API | [WEBSERVICES.md](../demo/docs/WEBSERVICES.md) |
| `/services/fixtures/graphql.py` | Test fixture for GraphQL  | [WEBSERVICES.md](../demo/docs/WEBSERVICES.md) |

## Mocking
- In progress.