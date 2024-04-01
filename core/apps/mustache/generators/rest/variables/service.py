from core.web.services.core.json import JsonObject


class MustacheTemplateService(JsonObject):
    resource: str
    base_module_path_generated_base: str
    base_module_path_models: str
    models: dict = {}
    operations: dict = {}
    uri: str
