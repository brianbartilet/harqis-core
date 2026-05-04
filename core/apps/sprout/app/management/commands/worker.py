from django.core.management.base import BaseCommand
from django.utils import autoreload

from .restart import restart_celery_worker

from core.apps.sprout.settings import APP_PACKAGE
from core.config.env_variables import ENV_WORKFLOW_AUTORELOAD
from core.config.env_variables import ENV_WORKFLOW_CONFIG
from core.config.env_variables import ENV_WORKFLOW_CONCURRENCY
from core.config.env_variables import ENV_WORKFLOW_QUEUE


def _autoreload_enabled() -> bool:
    return str(ENV_WORKFLOW_AUTORELOAD).strip().lower() in ("1", "true", "yes", "on")


def restart_celery_worker_tasks():
    """Restart the Celery worker for the workflow app.

    Returns the subprocess.Popen handle so the management command can
    wait() on it when running outside the autoreloader.
    """
    return restart_celery_worker(APP_PACKAGE, ENV_WORKFLOW_CONFIG,
                                 concurrency=ENV_WORKFLOW_CONCURRENCY,
                                 queue=ENV_WORKFLOW_QUEUE
                                 )


class Command(BaseCommand):
    """Start the Celery worker.

    Set WORKFLOW_AUTORELOAD=1 to enable Django's file-watch reloader
    (dev only). Default behaviour is a single long-lived spawn — every
    autoreload event respawns celery, and on Windows each respawn opens
    a new console window if the prior process isn't cleaned up.
    """

    def handle(self, *args, **options):
        if _autoreload_enabled():
            print('Starting celery worker with autoreload (WORKFLOW_AUTORELOAD=1)...')
            autoreload.run_with_reloader(restart_celery_worker_tasks)
            return
        print('Starting celery worker (autoreload disabled)...')
        proc = restart_celery_worker_tasks()
        # Block on the spawned celery so this management command stays
        # parent to its child — without wait() the launcher exits and
        # the celery worker becomes an orphan with no PID-traceable parent.
        if proc is not None and hasattr(proc, "wait"):
            proc.wait()
