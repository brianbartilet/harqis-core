# Web Services Testing Documentation

## Introduction
- This document outlines the core implementations to test various web services.
- Please refer to docstrings in the code for more information.

## Modules
### core.web.services.core
- `/core` - contains the core implementations to test various web services.
- `/core/clients` - defines the clients to interact with the web services.
- `/core/clients/base.py` - base interface for the clients.
- `/core/config` - define configurations for the web services.
- `/core/constants` - define constants for the web services.
- `/core/contracts` - define contracts of behaviour for dependencies for web services testing.
- `/core/request_builder` - define a chainable request builder for web services testing.
- `/core/json.py` - JSON utility functions.
- `/core/request.py` - base class for a web service request.
- `/core/response.py` - base class for a web service response.

### core.web.services.fixtures
- `/fixtures` - contains the reusable fixtures to test in scale various web services.
- `/fixtures/base.py` - base class for the fixtures.
- `/fixtures/rest.py` - RESTful fixtures for web services testing.
- `/fixtures/graphql.py` - GraphQL fixtures for web services testing.

### core.web.services.tests
- `/tests` - contains unit tests for the library.

### core.web.services.manager
- `/manager.py` - provide a service manager to facilitate web services.