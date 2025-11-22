from core.apps.es_logging.app.elasticsearch import log_result
from unittest import TestCase


class TestsElasticDecorator(TestCase):

    @log_result()
    def test_data_failed(self):
        raise Exception("This is a failed run")

    @log_result()
    def test_data_success(self):
        return 0
