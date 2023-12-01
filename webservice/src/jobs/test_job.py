import datetime as dt
import logging

from jobs import scheduler

log = logging.getLogger(__file__)

log.warning("importing test_job!")
@scheduler.scheduled_job('date', run_date=dt.datetime.utcnow() + dt.timedelta(seconds=10))
def test_job():
    print("test-job: hello, world")
log.warning("successfully imported test job!")