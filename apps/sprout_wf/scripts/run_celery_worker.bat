set ENV=PROD
set ENV_TASK_APP=DAILY_TASKS
start /high python.exe manage.py celery_worker_tasks