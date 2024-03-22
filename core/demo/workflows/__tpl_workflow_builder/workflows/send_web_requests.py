from core.apps.sprout.app.celery import SPROUT


@SPROUT.task()
def send_requests():

    return None
