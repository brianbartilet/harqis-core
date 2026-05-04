import os
import subprocess
import psutil


_IS_WIN = os.name == "nt"


def kill_celery_process(target_pid):
    """Kills a Celery process with the given PID.

    Matches both `celery` (Unix) and `celery.exe` (Windows) so the
    cleanup works on every platform — the prior name=='celery.exe'
    filter silently no-op'd on Linux/macOS.
    """
    try:
        target_pid = int(str(target_pid))
    except (TypeError, ValueError):
        return False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.pid == target_pid and proc.info.get('name') in ('celery', 'celery.exe'):
                if _IS_WIN:
                    subprocess.call(['taskkill', '/f', '/PID', str(target_pid)])
                else:
                    proc.terminate()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def _has_attached_console() -> bool:
    """True iff a Windows console is attached to the current process.

    Used to decide whether the spawned celery inherits our console
    (output flows there) or is suppressed with CREATE_NO_WINDOW
    (silent daemon when launched under pythonw.exe). Always True on
    Unix — there's no equivalent to CREATE_NO_WINDOW.
    """
    if not _IS_WIN:
        return True
    try:
        import ctypes
        return ctypes.windll.kernel32.GetConsoleWindow() != 0
    except (OSError, AttributeError):
        return False


def _spawn_detached(cmd):
    """Spawn celery, inheriting the parent's console when one exists.

    - Console attached (parent is python.exe with a window) → omit
      CREATE_NO_WINDOW so celery's stdout/stderr land in that window.
    - No console (parent is pythonw.exe) → keep CREATE_NO_WINDOW so
      celery doesn't trigger Windows to allocate a fresh console
      window. Without this gate, a session of file-watch autoreload
      can pile up dozens of empty console windows.

    CREATE_NEW_PROCESS_GROUP detaches the child from the parent's
    signal group so an upstream Ctrl-C doesn't cascade through.
    """
    if _IS_WIN:
        if _has_attached_console():
            flags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            flags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
        return subprocess.Popen(cmd, creationflags=flags, close_fds=True)
    return subprocess.Popen(cmd, start_new_session=True, close_fds=True)


def restart_celery_scheduler(app, task_file):
    """
    Restarts the Celery scheduler for the given app and task file.

    Args:
        app (str): The name of the Celery app.
        task_file (str): The name of the task file.

    Returns:
        subprocess.Popen: handle to the spawned celery beat process.
    """
    pid_file = f'pid.restart_celery_scheduler.{task_file.lower()}'

    target_process = read_pid_from_file(pid_file)
    if target_process:
        print(f"Target celery process id: {target_process}")
        if kill_celery_process(target_process):
            print("Old scheduler process killed.")

    cmd = ['celery', '-A', app, 'beat', '-l', 'info', '--pidfile=']
    proc = _spawn_detached(cmd)

    print(f"Saving celery process id: {proc.pid}")
    write_pid_to_file(pid_file, proc.pid)
    return proc


def restart_celery_worker(app, task_file, use_eventlet=False, concurrency=10, queue='default'):
    """
    Restarts the Celery worker for the given app and task file.

    Args:
        app (str): The name of the Celery app, e.g. "core.apps.sprout.app".
        task_file (str): Logical worker name, used in -n (e.g. "worker_reports").
        use_eventlet (bool): Whether to use eventlet for concurrency. If False, gevent is used.
        concurrency (int): The number of concurrent worker processes/greenlets.
        queue (str | list[str] | None): Queue name or list of queue names for -Q.
                                        If None, Celery's default queue config is used.

    Returns:
        subprocess.Popen: handle to the spawned celery worker process.
    """
    pid_file = f'pid.restart_celery_worker.{task_file.lower()}.{queue}'

    target_process = read_pid_from_file(pid_file)
    if target_process:
        print(f"Target celery process id: {target_process}")
        if kill_celery_process(target_process):
            print("Old worker process killed.")

    pool = 'eventlet' if use_eventlet else 'gevent'

    # Base command
    cmd = [
        'celery',
        '-A', app,
        'worker',
        '-l', 'info',
        '--concurrency', str(concurrency),
        '-n', f'{task_file}@%h',
        '-P', pool,
    ]

    # Optional queue(s)
    if queue:
        if isinstance(queue, (list, tuple, set)):
            queue = ",".join(queue)
        else:
            queue = str(queue)
        cmd += ['-Q', queue]
        print(f"Starting worker for queue(s): {queue}")

    proc = _spawn_detached(cmd)

    print(f"Saving celery process id: {proc.pid}")
    write_pid_to_file(pid_file, proc.pid)

    return proc


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
