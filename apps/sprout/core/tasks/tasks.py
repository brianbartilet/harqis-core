from workflows import *

from apps.sprout.core.tasks.apps.testing_tasks import *
from apps.sprout.core.celery import SPROUT
from apps.sprout.settings import TIME_ZONE, USE_TZ
from config.environment_variables import ENV_TASK_APP

"""
https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html


BUGS: https://github.com/eventlet/eventlet/issues/616

"""

CONFIG_DICTIONARY = {
    'MAP_TESTING_TASKS': MAP_TESTING_TASKS,

}

SPROUT.conf.beat_schedule = CONFIG_DICTIONARY[ENV_TASK_APP]

SPROUT.conf.enable_utc = USE_TZ
SPROUT.conf.timezone = TIME_ZONE
