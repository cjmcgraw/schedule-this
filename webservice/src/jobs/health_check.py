import datetime as dt
import dataclasses
import logging
import random
import time

from flask import abort, jsonify, request
from shared_memory_dict import SharedMemoryDict
from . import scheduler

log = logging.Logger(__file__)

log.info("starting up healthcheck process")

@dataclasses.dataclass(frozen=True)
class HealthState:
    msg: str
    at: dt.datetime
    took_ms: float

data = SharedMemoryDict(name="health_check_state", size=1024)


@scheduler.scheduled_job("interval", seconds=3, max_instances=1)
def run_health_check():
    log.info("starting healthcheck")
    start = time.time_ns()
    time.sleep(random.random())
    end = time.time_ns()
    data['state'] = HealthState(
        msg='green',
        at=dt.datetime.utcnow(),
        took_ms=round((end - start)/1e6, 4)
    )
    log.info("health state = {data}")