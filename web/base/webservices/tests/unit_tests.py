import unittest

from web.base.webservices import *

apps_config = {
    "NEW_APP": {

            "client": {
                "base_url": "https://api.youneedabudget.com/v1/",
                "response_encoding": "utf-8"
            }

    }
}


class BaseApiServiceTestApp(ApiService, Generic[T]):

    def __init__(self, source_id, **kwargs):
        super(BaseApiServiceTestApp, self)\
            .__init__(source_id=source_id,
                      apps_config_data=apps_config,
                      **kwargs)

class SubClassApiServiceTrello(BaseApiServiceTestApp):
    ...
class TestsUnitWebServices(unittest.TestCase):
    def test_run_unit_tests_mp(self):
        service = SubClassApiServiceTrello(source_id='NEW_APP')
