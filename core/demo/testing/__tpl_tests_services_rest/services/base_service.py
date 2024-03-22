from core.web.services.fixtures.rest import BaseFixtureServiceRest


class BaseServiceApp(BaseFixtureServiceRest):
    def __init__(self, config, **kwargs):
        super(BaseServiceApp, self).__init__(config=config, **kwargs)
