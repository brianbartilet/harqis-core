from config.environment_variables import ENV_TASK_APP
from django.core.management.base import BaseCommand
from django.utils import autoreload

from .restart import restart_celery_worker


def restart_celery_worker_tasks():
    """Restart the Celery scheduler for the workflow app."""
    restart_celery_worker('apps.sprout_wf.sprout', ENV_TASK_APP)


class Command(BaseCommand):
    """A Django management command to restart the Celery scheduler with autoreload."""

    def handle(self, *args, **options):
        """Handle the command execution."""
        print('Starting celery scheduler with autoreload...')
        # For Django>=2.2
        autoreload.run_with_reloader(restart_celery_worker_tasks)
