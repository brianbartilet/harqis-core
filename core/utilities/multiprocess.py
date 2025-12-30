import multiprocessing as mp
import psutil
from queue import Empty

from core.utilities.logging.custom_logger import create_logger


class MultiProcessingClient:
    """
    Multiprocessing helper that runs a function over a list of tasks in parallel.

    Notes:
    - Uses a spawn context (safer for Windows / pytest / Celery).
    - Supports an optional hard timeout; on timeout/error, terminates the pool so callers
      don't hang forever.
    - Keeps legacy queue/lock attributes for backward compatibility, but execute_tasks()
      uses Pool.map_async over self.tasks.
    """

    def __init__(self, tasks: list, worker_count=None):
        self.log = create_logger(self.__class__.__name__)
        cpu = psutil.cpu_count() or 1
        self.worker_count = int(worker_count) if worker_count else cpu

        # Legacy fields (not used by execute_tasks, but kept to avoid breaking imports/usages)
        self.queue = mp.Queue()
        self.tasks = list(tasks or [])
        self.output_list: list = []
        self.lock = mp.Lock()
        self.func = None
        self.add_tasks_to_queue()

    def add_tasks_to_queue(self):
        # Kept for compatibility; note execute_tasks uses self.tasks (not this queue).
        for task in self.tasks:
            self.queue.put(task)

    def execute_tasks(self, func, timeout_secs: int | None = None):
        """
        Executes tasks in parallel.

        Args:
            func: Top-level callable (must be picklable). Signature: func(task) -> result
            timeout_secs: Optional hard timeout for the *whole batch*. If exceeded, the
                         pool is terminated and the exception is raised.

        Returns:
            list: The results in the same order as self.tasks.
        """
        if not callable(func):
            raise TypeError("func must be callable")

        self.func = func
        self.output_list = []  # reset for this run

        ctx = mp.get_context("spawn")  # safest default on Windows/pytest/Celery
        pool = ctx.Pool(processes=self.worker_count)

        try:
            async_result = pool.map_async(func, self.tasks)

            # BLOCK until all results are ready (or timeout)
            results = async_result.get(timeout=timeout_secs) if timeout_secs else async_result.get()

            self.output_list.extend(results)

            pool.close()
            pool.join()

            return self.output_list

        except Exception:
            # IMPORTANT: ensure we don't hang forever
            self.log.exception("Multiprocessing execution failed; terminating pool")
            pool.terminate()
            pool.join()
            raise

    def worker_wrapper(self, func, args):
        """
        Worker function that processes tasks from the queue and stores results in output_list.

        Args:
            func (callable): The function to execute for each task.
            args (tuple): Additional arguments to pass to `func`.
        """
        while not self.queue.empty():
            try:
                task = self.queue.get(timeout=5)
                output = func(task, *args)
                with self.lock:
                    self.output_list.append(output)
            except Empty:
                break
            except Exception:
                self.log.exception("Error executing task in worker_wrapper")

    def get_tasks_output(self):
        """
        Returns the collected outputs from all processed tasks.

        Returns:
            list: Outputs of all executed tasks.
        """
        return self.output_list
