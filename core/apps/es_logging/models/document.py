from core.web.services.core.json import JsonObject
from datetime import datetime


update_interval_map = {
    #  handle multiple results posted to an interval to a unique location key
    "WEEKLY": datetime.now().strftime('%Y%m%d_%V'),
    "DAILY": datetime.now().strftime('%Y%m%d'),
    "HOURLY_4": datetime.now().strftime('%Y%m%d%H') + '4H',
    "HOURLY": datetime.now().strftime('%Y%m%d%H'),
    "MINUTE": datetime.now().strftime('%Y%m%d%H%M'),

}


class DtoElasticHitsSource(JsonObject):
    _index = str
    _id = str
    _source = []


class DtoElasticHits(JsonObject):
    total = dict
    max_score = int
    hits = [DtoElasticHitsSource]


class DtoElasticDocument(JsonObject):
    took = int
    timed_out = bool
    hits = DtoElasticHits


class DtoFunctionLogger(JsonObject):
    name = ''
    passed = 0.00
    failed = 0.00
    last_failed = None
    pass_fail_percent = 0.00
    short_name = ''
    exception_message = ''
    args = ''

    def compute_stat(self):
        self.pass_fail_percent = 100 * (self.passed / (self.passed + self.failed))
        self.short_name = self.name.split('.')[-1]

