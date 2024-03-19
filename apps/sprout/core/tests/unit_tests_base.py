from unittest import TestCase, mock
from apps.sprout.core.management.commands.scheduler import Command


class TestRestartCelerySchedulerTasks(TestCase):

    @mock.patch('apps.sprout.core.management.commands.scheduler.autoreload.run_with_reloader')
    @mock.patch('apps.sprout.core.management.commands.scheduler.restart_celery_scheduler_tasks')
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

