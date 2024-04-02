from core.web.services.core.json import JsonObject


class MustachePyTemplate(JsonObject):
    path: str
    docs: {}
    imports: {}
    classes: {}
    functions: {}
    args: {}
    tests: {}
    data: {}
