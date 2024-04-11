from core.utilities.data.strings import convert_to_snake_case, convert_dict_values_to_snake
from core.utilities.data.qlist import QList
from codegen.mustache.generators.rest import MustacheTemplateTestCase, MustacheTemplateTestStep


from http import HTTPStatus


def find_refs_in_dict(data, ref_key='$ref', found_refs=None):
    """
    Recursively search for occurrences of a specific key in a nested dictionary
    and collect their unique values.

    Args:
        data (dict | list): The input dictionary or list to search through.
        ref_key (str): The key to search for. Defaults to '$ref'.
        found_refs (set): Accumulator for found references, ensuring uniqueness. Should be None when called externally.

    Returns:
        list: A list of unique values associated with the specified key.
    """
    if found_refs is None:
        found_refs = set()

    if isinstance(data, dict):
        for key, value in data.items():
            if key == ref_key:
                value = value.split('/')[-1]  # Extract the reference name from the URL
                found_refs.add(value)  # Using set.add() ensures uniqueness
            else:
                find_refs_in_dict(value, ref_key, found_refs)
    elif isinstance(data, list):
        for item in data:
            find_refs_in_dict(item, ref_key, found_refs)

    return list(found_refs)  # Convert the set back to a list for the return value


def transform_types(openapi_spec: dict, type_mapping=None):
    """
    Recursively transforms 'type' fields within dictionaries from string identifiers to Python built-in types,
    and converts 'example' values to their corresponding representation based on the type. Handles nested
    structures like lists and dictionaries.

    Args:
        openapi_spec (dict): The input dictionary possibly containing nested structures with 'type' and 'example' fields.
        type_mapping (dict, optional): Mapping of type string identifiers to Python built-in types.
            Defaults to a predefined mapping if None is provided.

    Returns:
        dict: A dictionary with 'type' fields transformed to Python built-in type objects, and
              'example' values converted according to their 'type'.

    Example:
        >>> example_data = {
                'user': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string', 'example': '1'},
                        'completed': {'type': 'boolean', 'example': False}
                    }
                }
            }
        >>> print(transform_types(example_data))
        {
            'user': {
                'type': 'dict',
                'properties': {
                    'id': {'type': 'str', 'example': "'1'"},
                    'completed': {'type': 'bool', 'example': False}
                }
            }
        }
    """
    if type_mapping is None:
        type_mapping = {
            "string": str,
            "boolean": bool,
            "integer": int,
            "number": float,
            "array": list,
            "object": dict,
            "null": type(None),
        }

    def convert_example(example, type_key):
        if type_key == "string":
            return f'"{example}"'  # Using double quotes for string examples
        return example

    def transform_dict(d):
        if isinstance(d, dict):
            if 'type' in d and d['type'] in type_mapping:
                type_class = type_mapping[d['type']]
                transformed = {'type': type_class.__name__}
                if 'example' in d:
                    transformed['example'] = convert_example(d['example'], d['type'])
                if d['type'] == 'object' and 'properties' in d:
                    transformed['properties'] = transform_dict(d['properties'])
                if d['type'] == 'array' and 'items' in d:
                    transformed['items'] = transform_dict(d['items'])
                return transformed
            else:
                return {k: transform_dict(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [transform_dict(item) for item in d]
        else:
            return d

    return transform_dict(openapi_spec)


def transform_models(openapi_spec: dict):
    """
    Extracts model names from the OpenAPI specification and transforms them into a standardized format.

    This function searches for all references ($ref) within the OpenAPI spec to identify models. It then
    generates a list of dictionaries for each model, mapping the original model name to a snake_case
    version for use in code, and preserving the original name for reference.

    Args:
        openapi_spec (dict): The input dictionary containing an OpenAPI specification.

    Returns:
        list: A list of dictionaries, each containing 'model_name' and 'model_class_name' keys, where
              'model_name' is the snake_case version of the model's name, and 'model_class_name' is the
              original name of the model as found in the OpenAPI specification.

    Example:
        >>> openapi_spec = {'components': {'schemas': {'MyModel': {'type': 'object'}}}}
        >>> transform_models(openapi_spec)
        [{'model_name': 'my_model', 'model_class_name': 'MyModel'}]
    """
    schemas = find_refs_in_dict(openapi_spec)
    models = [{"name": convert_to_snake_case(name), "class_name": name} for name in schemas]

    return models


def group_paths_by_resource(open_api_spec: dict) -> dict:
    """
    Groups paths by their resource in the given OpenAPI data.

    Args:
        open_api_spec (dict): The input dictionary containing OpenAPI paths.

    Returns:
        dict: A dictionary where each key is a resource group prefix and its value is another
              dictionary with the paths and their details under that resource.
    """
    # Use a dictionary to hold groups, where each key represents a group prefix
    grouped = {}

    for key, value in open_api_spec.items():
        # Determine the group prefix (e.g., '/tasks')
        group_prefix = key.split('/')[1]  # Assumes there's at least one '/' in the key
        group_prefix = '/' + group_prefix  # Re-add leading slash for clarity

        if group_prefix not in grouped:
            grouped[group_prefix] = {}

        # Add the path and its details to the corresponding group
        grouped[group_prefix][key] = value

    return grouped


def transform_paths(resource: dict):
    """
    Transforms the paths in a resource dictionary from an OpenAPI specification into a more manageable format.

    This function iterates over each path and its operations within the provided resource dictionary,
    transforming details about responses and parameters. It standardizes operation IDs to snake_case,
    categorizes parameters as either path or query parameters, checks for the existence of request bodies,
    and assigns response hooks based on the operation's responses.

    Args:
        resource (dict): A dictionary where keys are paths and values are dictionaries of operations
                         and their details as specified in an OpenAPI document.

    Returns:
        list: A list of dictionaries, each representing an operation with keys like 'operation_id',
              'method', 'description', 'parameters', 'hasPayload', 'payloadSchema', 'hasResponseHook',
              and 'response_hook' providing details about the operation.

    Example:
        >>> resource = {
                '/pets': {
                    'get': {
                        'operationId': 'listPets',
                        'summary': 'List all pets',
                        'responses': {...},
                        'parameters': [...]
                    }
                }
            }
        >>> operations = transform_paths(resource)
        >>> print(operations[0]['operation_id'])  # Outputs: list_pets
        """
    def transform_response_hook(data: dict):
        success_codes = [HTTPStatus.OK, HTTPStatus.CREATED]
        response_200 = QList(data['responses']).where(lambda r: r in ''.join(str(i) for i in success_codes)).first()
        schema = data['responses'][response_200]['content']['application/json']['schema']

        if 'type' in schema.keys() and schema['type'] == 'list':
            response_hook = f'list[{find_refs_in_dict(schema['items'])[0]}]'.replace("'", "")
        elif 'type' not in schema.keys():
            response_hook = find_refs_in_dict(schema)[0]
        else:
            response_hook = 'dict'

        return response_hook

    def transform_parameters(data: dict) -> list:
        parameters = []
        if 'parameters' in data.keys():
            keys = list(data['parameters'])
            for i, param in enumerate(keys):
                param = convert_dict_values_to_snake(param)

                if 'in' in param.keys():
                    if param['in'] == 'path':
                        param['inPath'] = True
                    if param['in'] == 'query':
                        param['inQuery'] = True

                param['not_last'] = False if param == keys[-1] else True

                parameters.append(param)

        return parameters

    def get_payload_schema(data: dict):
        if 'requestBody' in data.keys():
            schema = data['requestBody']['content']['application/json']['schema']
            return find_refs_in_dict(schema)[0]
        return None

    # Extract operations and their details
    operations = []
    for path, methods in resource.items():
        for method, details in methods.items():
            operation = {
                "operation_id": convert_to_snake_case(details.get("operationId")),
                "method": method.upper(),
                "description": details.get("summary") if details.get("summary") else details.get("description"),
                "parameters": transform_parameters(details),
                "hasPayload": "requestBody" in details,
                "payloadSchema": get_payload_schema(details),
                "hasResponseHook": True,
                "response_hook": transform_response_hook(details),
                "responses": details['responses']
            }
            operations.append(operation)

    return operations


def transform_tests(resource, operations: list,
                    test_suite_name: str = 'sanity',
                    tags: list = None, test_technique: str = 'api'):
    tests = []

    for operation in operations:
        when = []
        then = []

        when_step_data: MustacheTemplateTestStep.data = {}

        if operation['method'] in ['GET', 'DELETE']:
            when_step_data = {
                'name': operation['operation_id'],
            }
        if operation['method'] in ['POST', 'PUT', 'PATCH']:
            when_step_data = {
                'name': operation['operation_id'],
                'has_payload': operation['hasPayload'],
                'payload': {
                    'name': operation['operation_id'],
                    'class_name': operation['payloadSchema']
                }
            }

        step_when = MustacheTemplateTestStep(data=when_step_data, args=operation['parameters'])
        when.append(step_when.get_dict())

        then_step_data: MustacheTemplateTestStep.data = {
            'http_status': QList(operation['responses'].keys()).first()
        }
        step_then = MustacheTemplateTestStep(data=then_step_data)
        then.append(step_then.get_dict())

        data: MustacheTemplateTestCase.data = {
            'service_name': resource,
        }
        test = MustacheTemplateTestCase(
            name=operation['operation_id'],
            description=operation['description'],
            test_suite_name=test_suite_name,
            test_technique=test_technique,
            tags=tags,
            given=[],
            when=when,
            then=then,
            status=None,
            data=data

        )
        tests.append(test.get_dict())

    return tests
