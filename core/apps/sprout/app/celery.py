from celery import Celery
from core.apps.config import AppConfig, AppNames

apps_config = AppConfig(AppNames.TASKS_CLIENT, dict).config
SPROUT = Celery(apps_config['application_name'], broker=apps_config['broker'])

