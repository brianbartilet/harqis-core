import pytest
from hamcrest import assert_that, greater_than_or_equal_to
from core.apps.es_logging.app.elasticsearch import (
    post,
    get_index_data,
    )
from unittest import TestCase
from uuid import uuid4

from  core.web.services.core.json import JsonObject

class TestData(JsonObject):
    blur = None
    borg = None
    mulch = None

index_name = '{0}'.format("harqis-testing").lower()

class TestsElastic(TestCase):

    @pytest.mark.skip(reason="just for manual testing")
    def test_data(self):
        test_id = '{0}'.format(uuid4())
        json_dump = TestData(borg="help", blur="test", mulch="orly")
        post(json_dump.get_dict(), index_name, test_id)

        data = get_index_data(index_name=index_name, type_hook=TestData, search_string="help")
        assert_that(len(data), greater_than_or_equal_to(0))


