from core.web.services.core.constants.http_methods import HttpMethod

from core.web.services.fixtures.rest import BaseFixtureServiceRest


class SimpleTestFixtureResourceOne(BaseFixtureServiceRest):

    def __init__(self, config):
        super(SimpleTestFixtureResourceOne, self).__init__(config)
        self.request.add_uri_parameter('posts')

    def get_request(self):
        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter('1')

        return self.client.execute_request(self.request.build())


class SimpleTestFixtureResourceTwo(SimpleTestFixtureResourceOne):
    def __init__(self, config):
        super(SimpleTestFixtureResourceTwo, self).__init__(config)
        self.request.add_uri_parameter('posts')


class SimpleTestFixtureResourceThree(SimpleTestFixtureResourceOne):

    def __init__(self, config):
        super(SimpleTestFixtureResourceThree, self).__init__(config)
        self.request.add_uri_parameter('posts')

