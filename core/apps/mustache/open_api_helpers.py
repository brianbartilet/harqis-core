from core.utilities.data.strings import convert_to_snake_case


def transform_types(openapi_spec_parsed: dict, type_mapping=None):
    """
    Transforms 'type' fields within dictionaries from string identifiers to Python built-in types,
    and converts 'example' values to their corresponding representation based on the type.

    Args:
        openapi_spec_parsed (dict): The input dictionary containing properties with 'type' and 'example' fields.
        type_mapping (dict, optional): Mapping of type string identifiers to Python built-in types.
            Defaults to a predefined mapping if None is provided.

    Returns:
        dict: A dictionary with 'type' fields transformed to Python built-in type objects, and
        'example' values converted according to their 'type'.

    Example:
        >>> example_data = {
                'id': {'type': 'string', 'example': '1'},
                'completed': {'type': 'boolean', 'example': False}
            }
        >>> print(transform_types(example_data))
        {'id': {'type': 'str', 'example': "'1'"}, 'completed': {'type': 'bool', 'example': False}}
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

    # Function to convert example values based on type
    def convert_example(example, type_key):
        if type_key == "string":
            # Properly format string literals with single quotes
            return '\"{}\"'.format(example)
        return example

    transformed_data = {}
    for key, prop in openapi_spec_parsed.items():
        if 'type' in prop and prop['type'] in type_mapping:
            type_class = type_mapping[prop['type']]
            transformed_prop = prop.copy()
            transformed_prop['type'] = type_class.__name__
            # Convert 'example' value if it exists
            if 'example' in prop:
                transformed_prop['example'] = convert_example(prop['example'], prop['type'])
            transformed_data[key] = transformed_prop
        else:
            transformed_data[key] = prop

    return transformed_data


def transform_paths(resource_grouping: dict):
    # Extract operations and their details
    operations = []
    for path, methods in resource_grouping.items():
        for method, details in methods.items():
            operation = {
                "operation_id": convert_to_snake_case(details.get("operationId")),
                "method": method.upper(),
                "description": details.get("summary"),
                "parameters": [],  # Simplified; parameters extraction would be here
                "hasPayload": "requestBody" in details,
                "hasResponseHook": False,  # Simplified; set based on your needs
            }
            operations.append(operation)

    # Assuming models are directly under components.schemas for simplification

    return operations


def transform_models(openapi_spec_parsed: dict):
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

    schemas = find_refs_in_dict(openapi_spec_parsed)
    models = [{"model_name": convert_to_snake_case(name), "model_class_name": name} for name in schemas]

    return models


def group_paths_by_resource(data: dict) -> dict:
    """
    Groups paths by their resource in the given OpenAPI data.

    Args:
        data (dict): The input dictionary containing OpenAPI paths.

    Returns:
        dict: A dictionary where each key is a resource group prefix and its value is another
              dictionary with the paths and their details under that resource.
    """
    # Use a dictionary to hold groups, where each key represents a group prefix
    grouped = {}

    for key, value in data.items():
        # Determine the group prefix (e.g., '/tasks')
        group_prefix = key.split('/')[1]  # Assumes there's at least one '/' in the key
        group_prefix = '/' + group_prefix  # Re-add leading slash for clarity

        if group_prefix not in grouped:
            grouped[group_prefix] = {}

        # Add the path and its details to the corresponding group
        grouped[group_prefix][key] = value

    return grouped



