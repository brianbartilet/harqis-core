# HARQIS-core OpenAI Integration
This is the integration module of OpenAI GPT capabilities into the HARQIS-core platform.
This module is responsible for the communication with the OpenAI API and the processing of the responses.

## Setup
- An OpenAI API key is required to use this module. You can get one by signing up at https://beta.openai.com/signup/

## Modules
- `\assistants` - contains the classes that represent the different types of assistants that can be used in the platform.
- `\assistants\base.py` - contains the base class for all assistants.
- `\constants.py` - contains the constants used in the module.
- `\contracts` - interfaces to be implemented for behaviour of GPT objects.
- `\models` - data models used in the module.
- `\services` - contains the classes that handle the communication with the OpenAI API.
- `\tests` - contains the tests for the module.