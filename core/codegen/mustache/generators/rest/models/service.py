from core.codegen.mustache.generators.base.py_template import MustachePyTemplate
from typing import Dict


class MustacheTemplateService(MustachePyTemplate):
    imports = {
        'path': str,
        'models': {
            'path': str,
            'items': [Dict[str, str]]
        }
    }
    classes = {
        'name': str,
        'uri': str,
        'functions': {
            'operation_id': str,
            'description': str,
            'method': str,
            'args': {},
        },

    },
    openapi = {}
