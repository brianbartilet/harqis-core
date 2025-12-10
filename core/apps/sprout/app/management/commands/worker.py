from django.core.management.base import BaseCommand
from django.utils import autoreload

from .restart import restart_celery_worker

from core.apps.sprout.settings import APP_PACKAGE
from core.config.env_variables import ENV_WORKFLOW_CONFIG
from core.config.env_variables import ENV_WORKFLOW_CONCURRENCY
from core.config.env_variables import ENV_WORKFLOW_QUEUE


def restart_celery_worker_tasks():
    """Restart the Celery scheduler for the workflow app."""
    restart_celery_worker(APP_PACKAGE, ENV_WORKFLOW_CONFIG,
                          concurrency=ENV_WORKFLOW_CONCURRENCY,
                          queue=ENV_WORKFLOW_QUEUE
                          )


class Command(BaseCommand):
    """A Django management command to restart the Celery scheduler with autoreload."""

    def handle(self, *args, **options):
        """Handle the command execution."""
        print('Starting celery scheduler with autoreload...')
        # For Django>=2.2
        autoreload.run_with_reloader(restart_celery_worker_tasks)
