from core.web.services.core.json import JsonObject
from typing import List, Dict


class MustacheTemplateConfigYaml(JsonObject):
    """
    Represents a model for a Mustache template.

    This Model is designed to capture the structure necessary for rendering
    Mustache templates, particularly focusing on the objects and their properties
    that the template will utilize.

    Attributes:
        application_name (str): The name of the application.
        base_url (str): The base URL of the API.
        response_encoding (str): The encoding of the response.
    """
    application_name: str
    base_url: str
    response_encoding: str
