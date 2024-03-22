from core.apps.sprout.app.celery import SPROUT


@SPROUT.task()
def wf_cross_application_web_request():

    return None
