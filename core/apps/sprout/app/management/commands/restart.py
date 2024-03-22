import subprocess
import psutil


def kill_celery_process(target_pid):
    """Kills a Celery process with the given PID."""
    for proc in psutil.process_iter():
        if proc.name() == 'celery.exe' and str(proc.pid) == target_pid:
            subprocess.call(['taskkill', '/f', '/PID', target_pid])
            return True
    return False


def restart_celery_scheduler(app, task_file):
    """
    Restarts the Celery scheduler for the given app and task file.

    Args:
        app (str): The name of the Celery app.
        task_file (str): The name of the task file.
    """
    pid_file = f'pid.restart_celery_scheduler.{task_file.lower()}'

    target_process = read_pid_from_file(pid_file)
    if target_process:
        print(f"Target celery process id: {target_process}")
        if kill_celery_process(target_process):
            print("Old scheduler process killed.")

    cmd = f'celery -A {app} beat -l info --pidfile='
    process = subprocess.Popen(cmd.split()).pid

    print(f"Saving celery process id: {process}")
    write_pid_to_file(pid_file, process)


def restart_celery_worker(app, task_file, use_eventlet=False, concurrency=10):
    """
    Restarts the Celery worker for the given app and task file.

    Args:
        app (str): The name of the Celery app.
        task_file (str): The name of the task file.
        use_eventlet (bool): Whether to use eventlet for concurrency.
        concurrency (int): The number of concurrent workers.
    """
    pid_file = f'pid.restart_celery_worker.{task_file.lower()}'

    target_process = read_pid_from_file(pid_file)
    if target_process:
        print(f"Target celery process id: {target_process}")
        if kill_celery_process(target_process):
            print("Old worker process killed.")

    pool = 'eventlet' if use_eventlet else 'gevent'
    cmd = f'celery -A {app} worker -l info --concurrency={concurrency} -n {task_file}@%h -P {pool}'
    process = subprocess.Popen(cmd.split()).pid

    print(f"Saving celery process id: {process}")
    write_pid_to_file(pid_file, process)


def read_pid_from_file(pid_file):
    """Reads and returns the PID from the specified file."""
    try:
        with open(pid_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def write_pid_to_file(pid_file, pid):
    """Writes the PID to the specified file."""
    with open(pid_file, 'w') as file:
        file.write(str(pid))

