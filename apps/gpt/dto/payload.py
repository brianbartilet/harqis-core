from web.services.core.json import JsonObject


class PayloadGPT(JsonObject):
    prompt: str = None
    model: str = None
    max_tokens: int = 100

