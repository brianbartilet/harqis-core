"""
This module is responsible for setting up and scheduling periodic tasks with Celery for executing web requests. It leverages Celery's ability to run tasks at specified intervals, automating the process of sending web requests as part of the application's workflow operations.

Scheduled tasks are defined in the `TASKS_DO_MATH` dictionary. Each entry in this dictionary specifies a unique task that is scheduled to run periodically. The configuration of these tasks includes the task function to be executed, the schedule of execution, and any arguments required by the task function.

Scheduled Task Configuration:
- `task`: A string that specifies the import path to the task function. This function is called each time the task is executed.
- `schedule`: A `datetime.timedelta` object that defines how often the task is executed. For example, a schedule of `timedelta(seconds=10)` means the task will run every 10 seconds.
- `args`: A list of arguments that will be passed to the task function upon execution. This list should match the expected arguments of the function.

Example:
The task 'run-test-sample-workflow-web-request' is configured to periodically execute the `send_requests` function found in the module `core.demo.workflows.__tpl_workflow_builder.workflows.send_web_requests`. It runs every 10 seconds without requiring any additional arguments (`'args': []`).

Usage:
To use this module, ensure Celery is properly set up and configured in your project. Then, incorporate the `TASKS_SEND_WEB_REQUESTS` dictionary into your Celery Beat schedule configuration to start scheduling these tasks.

References:
- For an overview of setting up periodic tasks with Celery, see the Celery documentation on Periodic Tasks: https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
- For solutions to common issues such as the Celery Beat UnpicklingError, consult: https://stackoverflow.com/questions/31468354/unpicklingerror-on-celerybeat-startup
"""


from datetime import timedelta

import random as r
from celery.schedules import crontab


"""
A dictionary mapping task identifiers to their configuration for scheduling.

This includes:
- 'task': The dotted path to the function to execute as a task.
- 'schedule': The frequency of execution, defined as a datetime.timedelta for recurring tasks.
- 'args': A list of arguments to pass to the task function.

Example task 'run-test-sample-workflow' is scheduled to run every 10 seconds, executing
the 'run_sample_workflow_add' function with specified arguments.
"""
TASKS_DO_MATH = {

    # region Tasks To Test

    'run-test-sample-workflow-math': {
        'task': 'core.demo.workflows.__tpl_workflow_builder.workflows.do_math.add',
        'schedule': timedelta(seconds=2),
        'args': [r.randint(1, 1000), r.randint(1, 1000)],
    },
    'run-test-sample-workflow-math-cron': {
        'task': 'core.demo.workflows.__tpl_workflow_builder.workflows.do_math.add',
        'schedule': crontab(minute='*', hour='*', day_of_week='mon,tue,wed,thu,fri'),
        'args': [r.randint(1, 2), r.randint(50, 100)],
    },

    # endregion
}
