# Sprout!
A simple Django app for running tasks

## Description
- This module is a simple Django app for managing tasks (a automation script) that can be run on a schedule.

## Dependencies
- Utilizes the [celery](https://docs.celeryproject.org/en/stable/) library for task scheduling and applying related decorators.
- Uses [RabbitMQ](https://www.rabbitmq.com/) as the message broker for celery.

## Modules
- `/app/management/commands` - contains the commands for the app for managing workers, schedule and restart.
- `/app/tests` - contains the tests for the app.
- `/app/manage.py` - the Django management script.
- `/app/helpers` - contains helper functions for the app.
-
## Demo
- Please see the application demo in the [demo](../../demo/workflows/README.md).