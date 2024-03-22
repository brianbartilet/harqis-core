from django.core.management.base import BaseCommand
from django.utils import autoreload

from .restart import restart_celery_scheduler

from core.apps.sprout.settings import APP_PACKAGE
from core.config.env_variables import ENV_WORKFLOW_CONFIG


def restart_celery_scheduler_tasks():
    """Restart the Celery scheduler for the workflow app."""
    restart_celery_scheduler(APP_PACKAGE, ENV_WORKFLOW_CONFIG)


class Command(BaseCommand):
    """A Django management command to restart the Celery scheduler with autoreload."""

    def handle(self, *args, **options):
        """Handle the command execution."""
        print('Starting celery scheduler with autoreload...')
        # For Django>=2.2
        autoreload.run_with_reloader(restart_celery_scheduler_tasks)
