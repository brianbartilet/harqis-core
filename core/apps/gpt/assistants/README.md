## OpenAPI Assistant Workflow
#### Initialize
- Search a given directory for all files with pattern and upload them files service
- Create a new thread

#### Add Messages
- Create messages to the thread to explain each of the files uploaded along with the folder structure, attach file id
    the file to the message
- Create message for the OpenAPI to be converted to tests, attach files related to fixtures along adding context to
    analyze the references and documentation
- Create a message to provide a folder structure to be generated run steps
- Add Python rules, e.g. tabs vs spaces, PEP 8, add docstrings
- pytest context

### Create Instruction
- CORE: generate code from the fixtures and examples provided, provide folder structure
- Create a md file for the full message

### Create A Run
- Wait for the run to complete
- Analyze run steps
- Check code patterns from markers e.g. and create files from code
  ```python
  import os
  import pytest
  ```
- Process file structure if possible
- Git ignore files generated from a `generated` folder

