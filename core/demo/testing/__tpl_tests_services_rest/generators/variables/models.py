from core.web.services.core.json import JsonObject
from typing import List, Dict


class MustacheTemplateModel(JsonObject):
    """
    Represents a model for a Mustache template.

    This Model is designed to capture the structure necessary for rendering
    Mustache templates, particularly focusing on the objects and their properties
    that the template will utilize.

    Attributes:
        object_name (str): The name of the object being described, which will
            be used within the Mustache template to reference this particular
            set of properties.
        properties (List[Dict[str, str]]): A list of dictionaries where each
            dictionary represents a property of the object. Each dictionary
            should have a 'name' key representing the property's name and a
            'type' key representing the property's data type as a string.
    """

    object_name: str
    properties: List[Dict[str, str]]
