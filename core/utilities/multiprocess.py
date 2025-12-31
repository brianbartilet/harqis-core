import multiprocessing as mp
import psutil
from queue import Empty

from core.utilities.logging.custom_logger import create_logger


class MultiProcessingClient:
    """
    Multiprocessing helper that runs a function over a list of tasks in parallel.

    Defaults to Pool.map_async over self.tasks (no mp.Queue/Lock created).
    If you truly need queue-based consumption, pass use_legacy_queue=True.
    """

    def __init__(self, tasks: list, worker_count=None, *, use_legacy_queue: bool = False):
        self.log = create_logger(self.__class__.__name__)
        cpu = psutil.cpu_count() or 1
        self.worker_count = int(worker_count) if worker_count else cpu

        self.tasks = list(tasks or [])
        self.output_list: list = []
        self.func = None

        # Legacy fields: ONLY create if explicitly requested
        self.queue = None
        self.lock = None
        self._use_legacy_queue = bool(use_legacy_queue)

        if self._use_legacy_queue:
            self._init_legacy_queue()

    def _init_legacy_queue(self):
        # Create legacy primitives only when needed
        self.queue = mp.Queue()
        self.lock = mp.Lock()
        for task in self.tasks:
            self.queue.put(task)

    def close(self):
        """
        Explicitly release legacy multiprocessing primitives (if created).
        Safe to call multiple times.
        """
        if self.queue is not None:
            try:
                self.queue.close()
                self.queue.join_thread()
            except Exception:
                pass
            self.queue = None

        self.lock = None

    def execute_tasks(self, func, timeout_secs: int | None = None):
        """
        Executes tasks in parallel using Pool.map_async over self.tasks.

        Args:
            func: Top-level callable (must be picklable). Signature: func(task) -> result
            timeout_secs: Optional hard timeout for the whole batch.

        Returns:
            list: results in the same order as self.tasks
        """
        if not callable(func):
            raise TypeError("func must be callable")

        self.func = func
        self.output_list = []

        ctx = mp.get_context("spawn")
        pool = ctx.Pool(processes=self.worker_count)

        try:
            async_result = pool.map_async(func, self.tasks)
            results = async_result.get(timeout=timeout_secs) if timeout_secs else async_result.get()

            self.output_list.extend(results)

            pool.close()
            pool.join()
            return self.output_list

        except Exception:
            self.log.exception("Multiprocessing execution failed; terminating pool")
            pool.terminate()
            pool.join()
            raise

        finally:
            # If legacy queue was created, ensure it can't keep pytest alive
            self.close()

            # Extra safety: reap any leftover children quickly
            try:
                for p in mp.active_children():
                    p.join(timeout=0.1)
            except Exception:
                pass

    def worker_wrapper(self, func, args):
        """
        Legacy queue-based worker loop. Only usable if use_legacy_queue=True.
        """
        if self.queue is None or self.lock is None:
            raise RuntimeError("worker_wrapper requires use_legacy_queue=True")

        while True:
            try:
                task = self.queue.get(timeout=5)
            except Empty:
                break
            except Exception:
                self.log.exception("Error reading from queue")
                break

            try:
                output = func(task, *args)
                with self.lock:
                    self.output_list.append(output)
            except Exception:
                self.log.exception("Error executing task in worker_wrapper")

    def get_tasks_output(self):
        return self.output_list
