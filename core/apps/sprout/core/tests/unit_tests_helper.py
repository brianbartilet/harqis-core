import unittest
import os
from unittest.mock import patch, MagicMock
from core.apps.sprout.core.management.commands.restart import restart_celery_scheduler, restart_celery_worker


class TestCeleryRestart(unittest.TestCase):

    def setUp(self):
        self.app = 'myapp'
        self.task_file = 'mytaskfile'
        self.scheduler_pid_file = f'pid.restart_celery_scheduler.{self.task_file.lower()}'
        self.worker_pid_file = f'pid.restart_celery_worker.{self.task_file.lower()}'

    def tearDown(self):
        if os.path.exists(self.scheduler_pid_file):
            os.remove(self.scheduler_pid_file)
        if os.path.exists(self.worker_pid_file):
            os.remove(self.worker_pid_file)

    @patch('core.apps.sprout.core.management.commands.restart.subprocess.Popen')
    @patch('core.apps.sprout.core.management.commands.restart.psutil.process_iter')
    def test_restart_celery_scheduler(self, mock_process_iter, mock_popen):
        mock_process = MagicMock()
        mock_process.pid = 1234
        mock_popen.return_value = mock_process

        restart_celery_scheduler(self.app, self.task_file)

        mock_popen.assert_called_once()
        self.assertTrue(os.path.exists(self.scheduler_pid_file))

        with open(self.scheduler_pid_file, 'r') as file:
            pid = file.read().strip()
            self.assertEqual(pid, '1234')

    @patch('core.apps.sprout.core.management.commands.restart.subprocess.Popen')
    @patch('core.apps.sprout.core.management.commands.restart.psutil.process_iter')
    def test_restart_celery_worker(self, mock_process_iter, mock_popen):
        mock_process = MagicMock()
        mock_process.pid = 5678
        mock_popen.return_value = mock_process

        restart_celery_worker(self.app, self.task_file, use_eventlet=True, concurrency=5)

        mock_popen.assert_called_once()
        self.assertTrue(os.path.exists(self.worker_pid_file))

        with open(self.worker_pid_file, 'r') as file:
            pid = file.read().strip()
            self.assertEqual(pid, '5678')