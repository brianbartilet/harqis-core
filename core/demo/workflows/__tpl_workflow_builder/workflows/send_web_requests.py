from core.apps.sprout.app.celery import SPROUT
from uuid import uuid4


@SPROUT.task()
def send_requests():

    return uuid4()
