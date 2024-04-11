from core.codegen.mustache.generators.base.py_template import MustachePyTemplate


class MustacheTemplateConfigYaml(MustachePyTemplate):
    data = {
        'application_name': str,
        'base_url': str,
        'response_encoding': str
    }



