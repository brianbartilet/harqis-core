from datetime import timedelta

from cron_descriptor import get_description
from celery.schedules import crontab, schedule as celery_schedule


def get_cron_string(celery_cron):
    """
    Retrieve a cron expression from any Celery crontab object.
    Supports Celery 4.x → 5.x+.
    """
    # 1) Newer Celery
    if hasattr(celery_cron, "as_cron"):
        return celery_cron.as_cron()

    # 2) Older Celery
    if hasattr(celery_cron, "to_string"):
        return celery_cron.to_string()

    # 3) Some Celery versions store original entry
    if hasattr(celery_cron, "_orig_entry"):
        return celery_cron._orig_entry

    # 4) FINAL fallback — Celery crontab.__str__ gives '*/10 * * * *'
    cron_str = str(celery_cron).strip()

    # Example __str__:
    # "<crontab: */10 * * * * (m/h/dM/MY/d)>"
    # We need to extract just the schedule.
    if cron_str.startswith("<crontab:"):
        # extract inside part before "("
        cron_inner = cron_str.split("<crontab:", 1)[1].split("(", 1)[0]
        return cron_inner.strip()

    # If __str__ is already clean, return it
    return cron_str


def _friendly_timedelta(td: timedelta) -> str:
    """
    Make a human-ish description from a timedelta.
    Examples: "Every 10 minutes", "Every hour", "Every 2 days".
    """
    total_seconds = int(td.total_seconds())
    if total_seconds <= 0:
        return "Runs immediately (no interval)"

    # Days?
    if td.days >= 1 and total_seconds % 86400 == 0:
        days = td.days
        return f"Every {days} day{'s' if days != 1 else ''}"

    # Hours?
    if total_seconds % 3600 == 0:
        hours = total_seconds // 3600
        return f"Every {hours} hour{'s' if hours != 1 else ''}"

    # Minutes?
    if total_seconds % 60 == 0:
        minutes = total_seconds // 60
        return f"Every {minutes} minute{'s' if minutes != 1 else ''}"

    # Fallback to seconds
    return f"Every {total_seconds} second{'s' if total_seconds != 1 else ''}"


def friendly_schedule(schedule_obj):
    """
    Create a friendly description for a Celery schedule, supporting:
      - crontab(...)
      - timedelta(...)
      - celery.schedules.schedule(run_every=...)
    """
    # crontab schedule
    if isinstance(schedule_obj, crontab):
        cron_str = get_cron_string(schedule_obj)
        return get_description(cron_str)

    # plain timedelta
    if isinstance(schedule_obj, timedelta):
        return _friendly_timedelta(schedule_obj)

    # celery.schedules.schedule (interval-based)
    if isinstance(schedule_obj, celery_schedule):
        run_every = getattr(schedule_obj, "run_every", None)
        if isinstance(run_every, timedelta):
            return _friendly_timedelta(run_every)
        # Some custom/other schedule types might store it differently
        return f"Custom Celery schedule: {schedule_obj!r}"

    # Unknown type
    return f"Unsupported schedule type: {type(schedule_obj).__name__}"
