import logging

from apscheduler.schedulers.background import BackgroundScheduler


log = logging.getLogger(__file__)
scheduler = BackgroundScheduler(logging=log)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)