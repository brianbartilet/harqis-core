from core.codegen.mustache.generators.base.py_template import MustachePyTemplate
from typing import List, Dict


class MustacheTemplateTestStep(MustachePyTemplate):
    name: str
    status: str
    args: Dict[str, str]
    data: {
        'has_payload': bool,
        'payload': {
            'name': str,
            'class_name': str,
        }
    }


class MustacheTemplateTestCase(MustachePyTemplate):
    name: str
    description: str
    test_suite_name: str
    tags: List[str]
    given: [MustacheTemplateTestStep]
    when: [MustacheTemplateTestStep]
    then: [MustacheTemplateTestStep]
    not_implemented: bool = True
    status: str


class MustacheTemplatePyTest(MustachePyTemplate):
    path: str
    docs = {
        'name': str,
        'description': str,
    },
    imports = {
        'services': {
            'path': str,
            'items': [Dict[str, str]]
        },
        'models': {
            'path': str,
            'items': [Dict[str, str]]
        }
    },
    tests = {
        'items': [MustacheTemplateTestCase]
    },
    functions = {
        'setup': {
            'service_name': str,
            'service_class_name': str,
        }
    }

    tests_sanity: [MustacheTemplateTestCase]
