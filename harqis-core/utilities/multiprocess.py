import multiprocessing as mp
import psutil

from utilities.logging.custom_logger import create_logger
from queue import Empty


# This class is used to handle multiprocessing tasks.
class MultiProcessingClient:
    # The constructor for the MultiProcessingClient class.
    # It initializes the worker count, queue, tasks, output list, lock, and function.
    # It also adds tasks to the queue.
    def __init__(self, tasks: list, worker_count=None):
        # Create a logger for this class
        self.log = create_logger(self.__class__.__name__)

        # Set the worker count to the provided value or the number of CPUs if not provided
        self.worker_count = worker_count or psutil.cpu_count()
        # Initialize a multiprocessing queue
        self.queue = mp.Queue()
        # Store the tasks to be executed
        self.tasks = tasks
        # Initialize an empty list to store the output of the tasks
        self.output_list = []
        # Initialize a lock for thread-safe operations
        self.lock = mp.Lock()
        # Initialize the function to be executed on the tasks to None
        self.func = None
        # Add the tasks to the queue
        self.add_tasks_to_queue()

    # This method adds tasks to the queue.
    def add_tasks_to_queue(self):
        # Iterate over the tasks and put each one in the queue
        for task in self.tasks:
            self.queue.put(task)

    # This method executes the tasks with the provided function using a pool of workers.
    def execute_tasks(self, func):
        # Create a pool of workers
        with mp.Pool(self.worker_count) as pool:
            # Map the function to the tasks and get the results
            results = pool.map(func, self.tasks)
            # Extend the output list with the results
            self.output_list.extend(results)

    # This method is a wrapper for the worker function.
    # It executes the function on the tasks in the queue and stores the output.
    def worker_wrapper(self, func, args):
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
        return self.output_list
