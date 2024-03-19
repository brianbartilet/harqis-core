from celery import Celery
from celery import Task

"""
from .AAA import *
from .BPI import *
from .BrewFather import *
from .CitisecOnline import *
from .CurrencyFreaks import *
from .EchoMTG import *
from .ELK import *
from .ExchangeRates import *
from .Google import *
from .Investagrams import *
from .Lazada import *
from .Nike import *
from .OANDA import *
from .PSEITools import *
from .PushBullet import *
from .PushNotifications import *
from .Rainmeter import *
from .StrenuousLife import *
from .Trello import *
from .TwelveDataTrading import *
from .YNAB import *
"""
"""
log = custom_logger()
app = Celery(apps_config['Celery']['application_name'], broker=apps_config['Celery']['broker'])


def workflow(app_sequence_list: []):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                log.info("Executing flow: {0}".format(' -> '.join(map(str, app_sequence_list.__str__))))
            except Exception as e:
                log.warning(f"Failed to recognize application workflow sequence. {e}")
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


"""
