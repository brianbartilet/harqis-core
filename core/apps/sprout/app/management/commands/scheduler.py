from django.core.management.base import BaseCommand
from django.utils import autoreload

from .restart import restart_celery_scheduler

from core.apps.sprout.settings import APP_PACKAGE
from core.config.env_variables import ENV_WORKFLOW_AUTORELOAD
from core.config.env_variables import ENV_WORKFLOW_CONFIG


def _autoreload_enabled() -> bool:
    return str(ENV_WORKFLOW_AUTORELOAD).strip().lower() in ("1", "true", "yes", "on")


def restart_celery_scheduler_tasks():
    """Restart the Celery scheduler for the workflow app.

    Returns the subprocess.Popen handle so the management command can
    wait() on it when running outside the autoreloader.
    """
    return restart_celery_scheduler(APP_PACKAGE, ENV_WORKFLOW_CONFIG)


class Command(BaseCommand):
    """Start the Celery beat scheduler.

    Set WORKFLOW_AUTORELOAD=1 to enable Django's file-watch reloader
    (dev only). Default behaviour is a single long-lived spawn (see
    worker.py for rationale).
    """

    def handle(self, *args, **options):
        if _autoreload_enabled():
            print('Starting celery scheduler with autoreload (WORKFLOW_AUTORELOAD=1)...')
            autoreload.run_with_reloader(restart_celery_scheduler_tasks)
            return
        print('Starting celery scheduler (autoreload disabled)...')
        proc = restart_celery_scheduler_tasks()
        if proc is not None and hasattr(proc, "wait"):
            proc.wait()
