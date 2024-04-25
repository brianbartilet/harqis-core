# Web Services Testing Documentation

## Introduction
- This document outlines the core implementations to test various web services.
- Please refer to docstrings in the code for more information.

## Core Objects
- **Driver**: browser driver to interact with web applications.
- **Browser**: target browser to run applications.
- **Page**: an object to contain information of web pages and composed of elements.
- **Element**: an object to contain information of web elements and locators.
- **Fixture**: a reusable object to test in scale various web applications
- **Configuration**: settings to define the behaviour of the driver.

## Modules
### core.web.browser.core
- `/core` - contains the core implementations to test browsers.

### core.web.browser.fixtures
- `/fixtures` - contains the reusable fixtures to test in scale various browsers.


### core.web.browser.tests
- `/tests` - contains unit tests for the library.
