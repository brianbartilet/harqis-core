# Transform and Generate Code Using Mustache
- [Mustache](https://mustache.github.io/) is a logic-less template syntax. It can be used for HTML, config files, source code - anything. It works by expanding tags in a template using values provided in a hash or object.
- This module organizes related transform code and generators for the [fixtures](../../docs/FEATURES.md#testing-fixtures) in HARQIS core.

## Modules
- `/contracts` - contains the configuration files for generation behavior.
- `/generators` - contains scripts and mustache template definitions for generating code.
- `/generators/base` - base behaviours and common patterns for a generator used for specific task (e.g. Python code generation, YAML generation).

## Current Fixture Support
- Listed below are currently supported fixtures in the HARQIS core for code generation
- Future code generation support would be added as new fixtures are added to the core.

| Generator | Description                                                               | Notes         |
|-----------|---------------------------------------------------------------------------|---------------|
| graphQL   | Generation from schema in [fixture](../web/services/fixtures/graphql.py)  | needs cleanup |
| REST      | OpenAPI code generation using [fixture](../web/services/fixtures/rest.py) |               |

## Notes
More about generators [here](https://open.spotify.com/track/592nTDJAy8AucV4KKIDCmA?si=e72a2f838127485b).