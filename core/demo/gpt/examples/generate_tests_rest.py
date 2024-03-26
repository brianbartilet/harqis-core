"""

Context:
    You're a QA engineer working on a REST API testing project. You have an OpenAPI specification that describes the
    API endpoints, request/response formats, and authentication requirements. You want to generate test code for each
    API endpoint based on the fixtures provided.

Steps:
    Step 1: Preprocessing OpenAPI Specification
    Objective: Prepare the OpenAPI specification from a JSON, YAML, or URL source for input to the AI assistant.
    Action: Parse the OpenAPI spec to extract essential details about API endpoints into a structured format.
        This step is crucial for simplifying the input to the AI assistant.

    Step 2: Utilize the Pre-trained AI Assistant
    Objective: Leverage the pre-trained AI assistant to understand and generate test code based on your OpenAPI spec.
    Action: Instead of teaching the AI your custom patterns, you'll rely on the assistant's existing knowledge.
        This step may involve refining your API spec format or adjusting your expectations based on the assistant's
        capabilities and the patterns it has been trained on.

    Step 3: Generating Test Code
    Objective: Use the pre-trained AI assistant to generate test code directly from the preprocessed OpenAPI spec.
    Action: Craft a prompt that includes the preprocessed API spec and any necessary context the assistant might need.
        Then, query the AI assistant for each API operation to generate the corresponding test code.

    Step 4: Post-processing and Saving Test Files
    Objective: Ensure the generated test code aligns with your requirements and save it as .py files.
    Action: Validate the generated test code, format it, and save it in the appropriate directory structure
        as .py files.

"""