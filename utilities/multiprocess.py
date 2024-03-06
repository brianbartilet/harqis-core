import sys, os
import time
import psutil
import multiprocessing as multiprocess
from utilities import custom_logger
import uuid
import functools
from queue import Empty

IS_FINISHED = False


def multiprocess_worker():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
            except Exception:
                pass
        return wrapper

    return decorator


class MultiProcessingClient:

    def __init__(self, tasks: [], default_wait_secs=10, worker_count=None):
        """
        :param tasks:
        :param default_wait_secs: main dependency, should be greater than average process execution time
        :param worker_count:
        """
        self.log = custom_logger(logger_name="Multi Process Client")
        self.default_wait = default_wait_secs
        self.worker_count = worker_count
        self.queue = multiprocess.Queue(0)
        self.tasks = tasks
        self.output_dict = multiprocess.Manager().dict()
        self.func = None

        self.add_tasks_to_queue()

    def worker_wrapper(self, func, queue_parameters, *args):
        while True:
            item = self.queue.get(block=True, timeout=None)
            queue_params = (item[i] for i in queue_parameters)

            output = func(*queue_params, *args)
            self.output_dict["result_{0}".format(uuid.uuid4())] = {item, output}

    def add_tasks_to_queue(self):
        if len(self.tasks) > 0:
            for task in self.tasks:
                self.queue.put(task, )

    def execute_tasks(self, func, *args):
        global IS_FINISHED

        self.func = func

        pool = multiprocess.Pool(self.get_cpu_count(), func, *args)
        pool.apply_async(self.stop_pool)

        self.execute_multiprocess_controller(self.queue)

        IS_FINISHED = True
        pool.terminate()
        pool.join()

    def get_tasks_output(self):
        output_list = []
        dict_ = dict(self.output_dict)
        for key in dict_:
            output_list.append(dict_[key])

        return output_list

    def stop_pool(self):
        while True:
            if IS_FINISHED:
                break
            time.sleep(1)

    def get_cpu_count(self):
        count = 1
        if self.worker_count is None:
            if sys.platform == 'win32':
                count = psutil.cpu_count()
        else:
            count = self.worker_count

        return count

    def execute_multiprocess_controller(self, queue):
        check = False

        while check is False:
            self.log.info("{0} :: Tasks Remaining in Queue: {1}".format(self.func.__name__, queue.qsize()))
            time.sleep(self.default_wait)
            if self.queue.qsize() == 0:
                break
