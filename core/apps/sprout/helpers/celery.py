import shelve
from datetime import datetime


def get_upcoming_scheduler_tasks(path='celerybeat-schedule'):
    """
    Retrieves a sorted list of upcoming tasks scheduled in a shelve database.

    The function opens a shelve database, reads the scheduled tasks, calculates
    the next run time for each task based on its last run time and the estimated
    remaining time until the next run. Tasks containing newlines or the word 'celery'
    in their names are ignored as they are likely to be metadata or default celery tasks.

    Args:
        path (str): The path to the shelve database file containing the scheduler tasks.
                    Defaults to 'celerybeat-schedule'.

    Returns:
        list of tuple: A list of tuples where each tuple contains:
                       (task_name, next_run_time), sorted by the next_run_time.
                       `task_name` is a string, `next_run_time` is a datetime object.

    Example:
        >>> get_upcoming_scheduler_tasks('my_scheduler_db')
        [('task1', datetime.datetime(2023, 10, 5, 14, 30)),
         ('task2', datetime.datetime(2023, 10, 5, 15, 0))]
    """
    db = shelve.open(path, writeback=True)

    entries = sorted(db['entries'])
    schedules = []
    for entry in entries:
        if '\n' in entry or 'celery' in entry:
            continue
        last_run = db['entries'][entry].last_run_at
        now = datetime.now()
        time_delta = db['entries'][entry].schedule.remaining_estimate(last_run)
        next_run = now - time_delta
        schedules.append((entry, next_run))

    db.close()

    return sorted(schedules, key=lambda x: x[1])
