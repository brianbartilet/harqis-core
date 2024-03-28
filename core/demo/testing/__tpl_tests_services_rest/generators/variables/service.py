from core.web.services.core.json import JsonObject


class MustacheTemplateService(JsonObject):
    base_module_path_services: str
    base_module_path_models: str
    models: dict = {}
    service_name: str
    get: dict = {}
    post: dict = {}
    patch: dict = {}
    delete: dict = {}
    put: dict = {}