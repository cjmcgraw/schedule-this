import datetime as dt
import importlib.util
import importlib
import logging
import atexit
import pathlib
import sys
import os

import flask
from flask_restful import Resource, Api
from flask_apscheduler import APScheduler

from jobs import scheduler, health_check

log = logging.getLogger(__file__)

log.warning("application starting up!")

jobs_dir = pathlib.Path(__file__).parent / "jobs"
jobs_to_import = [
    job
    for job in jobs_dir.glob('*.py')
    if job.name != '__init__.py'
    and job.name != 'health_check.py'
]
log.warning(f"found jobs to load: {jobs_to_import}")
for job in jobs_to_import:
    log.warning(f"{job} - importing")
    module_name = job.name.removeprefix('.py')
    spec = importlib.util.spec_from_file_location(module_name, job)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    log.warning(f"{job} - success")

app = flask.Flask("schedule-this")
app.config.update(
    SCHEDULER_API_ENABLED = True
)

flask_scheduler = APScheduler(scheduler=scheduler, app=app)
flask_scheduler.start()

@app.get("/health")
@app.get("/health/*")
def healthcheck():
    state = health_check.data.get('state')
    print(state)
    now = dt.datetime.utcnow()


    response = dict(
        msg=getattr(state, 'msg', None),
        at=getattr(state, 'at', None),
        now=getattr(state, 'took_ms', None),
    )
    
    if not state or now - state.at > dt.timedelta(minutes=10):
        return flask.jsonify(response), 500

    return flask.jsonify(response), 200
    

def cleanup():
    log.warning("shutting down and cleaning up")
    health_check.data.shm.close()
    health_check.data.shm.unlink()
    log.warning("finished shutdown process")

atexit.register(cleanup)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8123,
        debug=True,
    )