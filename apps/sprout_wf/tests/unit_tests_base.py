from unittest import TestCase, mock
from apps.sprout_wf.management.commands.worker import restart_celery_scheduler_tasks, Command


class TestRestartCelerySchedulerTasks(TestCase):
    @mock.patch('apps.sprout_wf.management.commands.base.restart_celery_scheduler')
    @mock.patch('os.environ.get')
    def test_restart_celery_scheduler_tasks(self, mock_env_get, mock_restart_celery_scheduler):
        """Test that restart_celery_scheduler_tasks calls restart_celery_scheduler with correct arguments."""
        # Setup
        mock_env_get.return_value = 'test_task_map'

        # Execute
        restart_celery_scheduler_tasks()

        # Assert
        mock_env_get.assert_called_once_with('ENV_TASK_APP', 'TASKS_MAP')
        mock_restart_celery_scheduler.assert_called_once_with('apps.sprout_wf', 'test_task_map')

    @mock.patch('apps.sprout_wf.management.commands.base.autoreload.run_with_reloader')
    @mock.patch('apps.sprout_wf.management.commands.base.restart_celery_scheduler_tasks')
    def test_handle(self, mock_restart_tasks, mock_run_with_reloader):
        """Test that the handle method starts the celery scheduler with autoreload."""
        # Instantiate the Command object
        command = Command()

        # Execute the handle method
        command.handle()

        # Assert
        mock_run_with_reloader.assert_called_once_with(mock_restart_tasks)

        # Verify that print is called (optional, requires sys.stdout to be mocked)
        # This step is optional and can be omitted if testing the print statement is not necessary.

