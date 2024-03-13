import unittest
from utilities.multiprocess import MultiProcessingClient


def sample_task(x):
    return x * x


class TestMultiProcessingClient(unittest.TestCase):
    def test_execute_tasks(self):
        tasks = [1, 2, 3, 4, 5, 6, 7, 8]
        client = MultiProcessingClient(tasks)
        client.execute_tasks(sample_task, )
        results = client.get_tasks_output()
        expected_results = [1, 4, 9, 16, 25, 36, 49, 64]
        self.assertCountEqual(results, expected_results)