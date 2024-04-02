from core.apps.mustache.generators.base.py_template import MustachePyTemplate
from typing import List, Dict


class MustacheTemplateModel(MustachePyTemplate):
    classes = {
        'name': str,
        'properties': List[Dict[str, str]]
    }

