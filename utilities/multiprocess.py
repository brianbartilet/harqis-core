import multiprocessing as mp
import psutil
import uuid

from utilities.logging.custom_logger import custom_logger

class MultiProcessingClient:
    def __init__(self, tasks: list, default_wait_secs=10, worker_count=None):
        self.log = custom_logger("MultiProcessClient")
        self.default_wait = default_wait_secs
        self.worker_count = worker_count or psutil.cpu_count()
        self.manager = mp.Manager()
        self.queue = self.manager.Queue()
        self.tasks = tasks
        self.output_dict = self.manager.dict()
        self.func = None
        self.add_tasks_to_queue()

    def add_tasks_to_queue(self):
        for task in self.tasks:
            self.queue.put(task)

    def execute_tasks(self, func, *args):
        self.func = func
        processes = []
        for _ in range(self.worker_count):
            p = mp.Process(target=self.worker_wrapper, args=(func, args))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

    def worker_wrapper(self, func, args):
        while not self.queue.empty():
            try:
                task = self.queue.get(timeout=5)
                output = func(task, *args)
                self.output_dict[f"result_{uuid.uuid4()}"] = output
            except self.queue.Empty:
                break
            except Exception as e:
                self.log.error(f"Error executing task: {e}")

    def get_tasks_output(self):
        return list(self.output_dict.values())
