import logging
import os
import subprocess

from core.utilities.multiprocess import MultiProcessingClient

except_folder_names = [
    '__pycache__',
    '__template',
    'common',
    'features',
    'venv'
]

file_pattern = 'unit_tests'


def run_cmd(item):
    """
    Run a test command in a subprocess.

    Args:
        item (str): The path to the test file to be executed.
    """
    print(f"Running tests in file: {item}")
    file = os.path.dirname(item)
    os.chdir(file)
    cmd = f'pytest {item}'
    subprocess.call(cmd, shell=True)


def worker_tests_mp(item):
    """
    Worker function for multiprocessing that gets test file paths from a queue and runs them.

    Args:
        item (str): The path to the test file to be executed.
    """
    run_cmd(item)


def workers_tests(queue):
    """
    Runs tests for each item in the queue.

    Args:
        queue (list): A list containing test file paths.
    """
    for item in queue:
        run_cmd(item)


class UnitTestLauncher:
    """
    A class for launching unit tests found in a specified directory and its subdirectories.
    """

    def __init__(self, **kwargs):
        """
        Initializes the UnitTestLauncher.

        Args:
            base_directory (str): The base directory to search for tests.
            tests_folder_name (str): The name of the folder containing tests.
            except_folder_names (list): A list of folder names to exclude from the search.
            multiprocessing (bool): A boolean indicating whether to use multiprocessing.
        """
        self.base_directory = kwargs.get('base_directory', os.getcwd())
        self.tests_folder_name = kwargs.get('tests_folder_name', 'tests')
        self.except_folder_names = kwargs.get('except_folder_names', except_folder_names)
        self.multiprocessing = kwargs.get('multiprocessing', False)

        self.kwargs = kwargs

    def run_tests(self):
        """
        Searches for test files matching a pattern and runs them.
        """
        found_test_files = []

        search = os.walk(self.base_directory)
        logging.info(f"Finding tests in base directory: {self.base_directory}")

        for path, sub_dirs, files in search:
            if self.tests_folder_name in path and not any(ext in path for ext in self.except_folder_names):
                # Check if any test files match the pattern in this directory
                current_dir_tests = [os.path.join(path, file) for file in files if
                                     file.endswith('.py') and file.startswith(file_pattern)]
                if len(current_dir_tests) > 0:
                    found_test_files.extend(current_dir_tests)
                else:
                    logging.info(f"Skipping {path}: No test files matching pattern '*{file_pattern}*' found.")

        logging.info(f"Found {len(found_test_files)} test directories")

        if self.multiprocessing:
            mp_client = MultiProcessingClient(tasks=found_test_files, worker_count=8)
            mp_client.execute_tasks(worker_tests_mp, )
        else:
            workers_tests(found_test_files)
