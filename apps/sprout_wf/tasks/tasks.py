from workflows import *

from apps.sprout_wf.tasks.apps.testing_tasks import *
from apps.sprout_wf.sprout import SPROUT
from config.environment_variables import ENV_TASK_APP

"""
https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html


BUGS: https://github.com/eventlet/eventlet/issues/616

"""

CONFIG_DICTIONARY = {
    'MAP_TESTING_TASKS': MAP_TESTING_TASKS,

}

SPROUT.conf.beat_schedule = CONFIG_DICTIONARY[ENV_TASK_APP]

SPROUT.conf.enable_utc = False
SPROUT.conf.timezone = 'Asia/Manila'
