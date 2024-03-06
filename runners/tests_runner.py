import logging

from utilities.multiprocess import *
import pytest
import subprocess, shlex

except_folder_names = [
    '__pycache__',
    '__template',
    'common',
    'features'
]

file = 'tests/unit_tests.py'


def run_cmd(item):
    print("Running runners on path: {0}".format(item))
    cmd_act_cfg = '"{0}" "{1}"'.format('pytest', '{0}\\{1}'.format(item, file))
    subprocess.call(shlex.split(cmd_act_cfg))


def worker_tests_mp(queue):
    while True:
        try:
            item = queue.get(block=False, timeout=None)
            run_cmd(item)
        except Empty:
            continue


def workers_tests(queue):
    for item in queue:
        run_cmd(item)


class UnitTestLauncher(object):

    def __init__(self, **kwargs):
        self.base_directory = kwargs.get('base_directory', os.getcwd())
        self.tests_folder_name = kwargs.get('tests_folder_name', 'tests')
        self.except_folder_names = kwargs.get('except_folder_names', except_folder_names)
        self.multiprocessing = kwargs.get('multiprocessing', False)

    def run_tests(self):
        found_directories = []

        search = os.walk(self.base_directory)
        logging.info("Finding tests on base directory: {0}".format(self.base_directory))

        for path, sub_dirs, files in search:
            if self.tests_folder_name in path and not any(ext in path for ext in self.except_folder_names):
                found_directories.append(path)
        logging.info("Found {} test directories".format(len(found_directories)))

        if self.multiprocessing:
            mp_client = MultiProcessingClient(tasks=found_directories,
                                              default_wait_secs=30,
                                              worker_count=4)
            mp_client.execute_tasks(worker_tests_mp, (mp_client.queue, ))
        else:
            workers_tests(found_directories)

