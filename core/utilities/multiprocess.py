import multiprocessing as mp
import psutil

from core.utilities.logging.custom_logger import create_logger
from queue import Empty


class MultiProcessingClient:
    """
    A class for handling multiprocessing tasks, allowing parallel execution of functions across multiple processes.

    Attributes:
        log: Logger object for logging information, errors, etc.
        worker_count (int): Number of worker processes to use.
        queue (mp.Queue): Multiprocessing queue to hold tasks to be processed.
        tasks (list): List of tasks to be executed.
        output_list (list): List to store outputs of the executed tasks.
        lock (mp.Lock): Lock for managing concurrent writes to the output_list.
        func (callable): The function to be applied to each task.
    """
    def __init__(self, tasks: list, worker_count=None):
        """
        Initializes the MultiProcessingClient with a list of tasks and optionally specifies the number of workers.

        Args:
            tasks (list): A list of tasks to be executed.
            worker_count (int, optional): The number of worker processes to use. Defaults to the number of CPUs available.
        """
        self.log = create_logger(self.__class__.__name__)
        self.worker_count = worker_count or psutil.cpu_count()

        self.queue = mp.Queue()
        self.tasks = tasks
        self.output_list = []
        self.lock = mp.Lock()
        self.func = None
        self.add_tasks_to_queue()

    def add_tasks_to_queue(self):
        """
        Adds tasks to the multiprocessing queue.
        """
        # Iterate over the tasks and put each one in the queue
        for task in self.tasks:
            self.queue.put(task)

    def execute_tasks(self, func):
        """
         Executes the tasks using a pool of workers and a specified function.

         Args:
             func (callable): The function to apply to each task.
         """
        # Create a pool of workers
        with mp.Pool(self.worker_count) as pool:
            # Map the function to the tasks and get the results
            results = pool.map(func, self.tasks)
            # Extend the output list with the results
            self.output_list.extend(results)

    def worker_wrapper(self, func, args):
        """
        Worker function that processes tasks from the queue and stores results in output_list.

        Args:
            func (callable): The function to execute for each task.
            args (tuple): Additional arguments to pass to `func`.
        """
        # While there are tasks in the queue
        while not self.queue.empty():
            try:
                # Get a task from the queue
                task = self.queue.get(timeout=5)
                # Execute the function on the task and get the output
                output = func(task, *args)
                # Add the output to the output list in a thread-safe manner
                with self.lock:
                    self.output_list.append(output)
            # If the queue is empty, break the loop
            except Empty:
                break
            # If an error occurs, log it
            except Exception as e:
                self.log.error(f"Error executing task: {e}")

    # This method returns the output of the tasks.
    def get_tasks_output(self):
        """
        Returns the collected outputs from all processed tasks.

        Returns:
            list: Outputs of all executed tasks.
        """
        return self.output_list
