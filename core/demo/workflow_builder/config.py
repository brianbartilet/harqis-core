"""
Configures the Celery app for scheduled tasks based on environment-specific settings.

This module initializes the Celery beat schedule using a configuration dictionary that maps task identifiers to their definitions. It dynamically selects the appropriate task mapping based on an environment variable, ensuring that tasks are scheduled according to environment-specific requirements. Additionally, it configures the Celery app to respect the timezone settings specified in the Django project settings, allowing for accurate scheduling of tasks across different timezones.

The configuration relies on external definitions for task mappings and environment variables to provide flexibility and modularity in defining task schedules.

References:
- Celery Periodic Tasks: https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html

Known Issues:
- Potential issues with Celery and Eventlet: https://github.com/eventlet/eventlet/issues/616
"""

from core.demo.workflow_builder.tasks.tasks_do_math import TASKS_DO_MATH
from core.demo.workflow_builder.tasks.tasks_send_web_requests import TASKS_SEND_WEB_REQUESTS

from core.apps.sprout.app.celery import SPROUT
from core.apps.sprout.settings import TIME_ZONE, USE_TZ

# Set Celery to use the same timezone settings as the Django project.
SPROUT.conf.enable_utc = USE_TZ
SPROUT.conf.timezone = TIME_ZONE

# Configuration dictionary mapping environment variable values to specific task mappings.
# Be careful to use duplicate keys in the dictionary, as it will overwrite the previous key.
CONFIG_DICTIONARY = TASKS_SEND_WEB_REQUESTS | TASKS_DO_MATH
# Configure the Celery beat schedule based on the current environment's task mapping.
SPROUT.conf.beat_schedule = CONFIG_DICTIONARY
