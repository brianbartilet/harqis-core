import multiprocessing as mp
import psutil

from utilities.logging.custom_logger import create_logger
from queue import Empty


class MultiProcessingClient:
    def __init__(self, tasks: list, worker_count=None):
        self.log = create_logger(self.__class__.__name__)

        self.worker_count = worker_count or psutil.cpu_count()
        self.queue = mp.Queue()
        self.tasks = tasks
        self.output_list = []
        self.lock = mp.Lock()
        self.func = None
        self.add_tasks_to_queue()

    def add_tasks_to_queue(self):
        for task in self.tasks:
            self.queue.put(task)

    def execute_tasks(self, func):
        with mp.Pool(self.worker_count) as pool:
            results = pool.map(func, self.tasks)
            self.output_list.extend(results)

    def worker_wrapper(self, func, args):
        while not self.queue.empty():
            try:
                task = self.queue.get(timeout=5)
                output = func(task, *args)
                with self.lock:
                    self.output_list.append(output)
            except Empty:
                break
            except Exception as e:
                self.log.error(f"Error executing task: {e}")

    def get_tasks_output(self):
        return self.output_list
