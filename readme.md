# The goal is simple. Run some jobs. Get outta the way!

We at ATG run many jobs inside of webservices. It is truly awful.

Lets make it better. Lets do one thing, but get good at it.

## How do?

I highly recommend learning about docker below. But you don't have to.

Open a terminal, run this. It will tail all the logs for you!
```
docker compose up
```

In another terminal window. Here are some commands you can use to interact
with this system. Its purpose is simple. It lets you run jobs. Write them
as scripts in the jobs directory.

# schedule api

* /scheduler [GET] > returns basic information about the webapp
* /scheduler/pause [POST] > pauses job processing in the scheduler
* /scheduler/resume [POST] > resumes job processing in the scheduler
* /scheduler/start [POST] > starts the scheduler
* /scheduler/shutdown [POST] > shuts down the scheduler with wait=True
* /scheduler/shutdown [POST] + json={‘wait’:False} post data > shuts down the scheduler with wait=False

# jobs api

* /scheduler/jobs [POST json job data] > adds a job to the scheduler
* /scheduler/jobs/<job_id> [GET] > returns json of job details
* /scheduler/jobs [GET] > returns json with details of all jobs


* /scheduler/jobs/<job_id> [DELETE] > deletes job from scheduler
* /scheduler/jobs/<job_id> [PATCH json job data] > updates an already existing job
* /scheduler/jobs/<job_id>/pause [POST] > pauses a job, returns json of job details
* /scheduler/jobs/<job_id>/resume [POST] > resumes a job, returns json of job details
* /scheduler/jobs/<job_id>/run [POST] > runs a job now, returns json of job details



## Getting Started

set modules envvars, or suffer defaults
```
# src/jobs/my_job.py
from . import scheduler

@scheduler.scheduled_task("interval", minutes=37, max_instances=1)
def run_job():
    ...
```


## Using this repo

To use this repo I highly recommend understanding the following commands:


Here we can take dockerfiles and make images. Images are like blue prints.
```
docker compose build
```

Here we can take images, and make containers.
```
docker compose create webservice
```

Here we can bring images up.
```
docker compose up webservice
```

All volume mounts should automatically be managed. You can run tests with

```
docker compose run tests
```
