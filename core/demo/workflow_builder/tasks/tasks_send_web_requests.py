"""
This module defines scheduled tasks for periodic execution using Celery.

Tasks are scheduled to run at specified intervals, handling various workflow operations.
The schedules and tasks are defined in the MAP_TESTING_TASKS dictionary. Each task
is associated with a specific function within the Workflows module and is configured
to run at a defined schedule.

References:
- Celery Periodic Tasks: https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
- Celery Beat UnpicklingError: https://stackoverflow.com/questions/31468354/unpicklingerror-on-celerybeat-startup
"""

from datetime import timedelta

import random as r
import datetime
from celery.schedules import crontab

TASKS_SEND_WEB_REQUESTS = {
    # region Tasks To Test

    'run-test-sample-workflow-web-request': {
        'task': 'core.demo.workflow_builder.workflows.workflows_example_group_web_requests.wf_cross_application_web_request',
        'schedule': timedelta(seconds=2),
        'args': [],
    },

    # endregion
}

"""
A dictionary mapping task identifiers to their configuration for scheduling.

This includes:
- 'task': The dotted path to the function to execute as a task.
- 'schedule': The frequency of execution, defined as a datetime.timedelta for recurring tasks.
- 'args': A list of arguments to pass to the task function.

Example task 'run-test-sample-workflow' is scheduled to run every 10 seconds, executing
the 'run_sample_workflow_add' function with specified arguments.
"""
