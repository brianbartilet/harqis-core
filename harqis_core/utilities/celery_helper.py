import shelve
from datetime import datetime


def get_upcoming_scheduler_tasks(path='celerybeat-schedule'):
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
