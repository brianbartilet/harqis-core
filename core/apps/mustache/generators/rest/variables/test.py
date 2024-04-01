from core.web.services.core.json import JsonObject


class MustacheTemplateTestCase(JsonObject):
    name: str
    description: str
    given: []
    when: []
    then: []
    not_implemented: bool = True


class MustacheTemplateTest(JsonObject):
    resource: str
    resource_camel: str
    modules: {
        'base_module_path_services': str,
        'resource': str,
        'resource_camel': str
    }
    base_module_path_generated: str
    tests_sanity: [MustacheTemplateTestCase]
    tests_integration: [MustacheTemplateTestCase]
    tests_negative: [MustacheTemplateTestCase]

