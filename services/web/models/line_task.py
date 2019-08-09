from datetime import timedelta

from web.models.job import Job
from web.resources import Db

import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LineTask:
    """Compose set of tasks according to iterations and time_sleep"""
    def __init__(
        self,
        exec_time,
        device_id,
        device_task_id,
        line_id,
        time,
        iterations,
        time_sleep,
        relay_num=-1,
        id=-1,
    ):
        self.id = id  # will be set after register into database
        self.line_id = line_id
        self.device_id = device_id
        self.device_task_id = device_task_id
        self.exec_time = exec_time
        self.time = time
        self.iterations = iterations
        self.time_sleep = time_sleep
        self.relay_num = relay_num

        self.jobs = list()

    @property
    def duration(self):
        return self.iterations * self.time + (self.iterations - 1) * self.time_sleep

    @property
    def time_ends(self):
        return self.exec_time + timedelta(minutes=self.duration)

    @property
    def next_rule_start_time(self):
        return self.time_ends + timedelta(minutes=self.duration * 2)

    def generate_jobs(self):
        exec_time = self.exec_time
        jobs = []
        for i in range(self.iterations):
            jobs.append(
                Job(
                    line_task_id=self.id,
                    line_id=self.line_id,
                    device_id=self.device_id,
                    desired_device_state=json.dumps(
                        {'state': {
                                  'relay': {'num': self.relay_num, 'state': 1}
                                  }
                        }),
                    exec_time=exec_time,
                )
            )
            jobs.append(
                Job(
                    line_task_id=self.id,
                    line_id=self.line_id,
                    device_id=self.device_id,
                    desired_device_state=json.dumps(
                        {'state': {
                                  'relay': {'num': self.relay_num, 'state': 0}
                                  }
                        }),
                    exec_time=exec_time + timedelta(minutes=self.time),
                )
            )
            exec_time = exec_time + timedelta(minutes=self.time_sleep)

        self.jobs = jobs

        return self

    def register(self):
        logger.info("Generating jobs")
        self.generate_jobs()

        q = """
               INSERT INTO line_tasks(line_id, device_task_id, device_id, exec_time, time, iterations, time_sleep)
               VALUES (%(line_id)s, %(device_task_id)s, %(device_id)s, %(exec_time)s, %(time)s, %(iterations)s, %(time_sleep)s)
               RETURNING id
               """
        self.id = Db.execute(query=q, params={'line_id': self.line_id,
                                              'device_task_id': self.device_task_id,
                                              'device_id': self.device_id,
                                              'exec_time': self.exec_time,
                                              'time': self.time,
                                              'iterations': self.iterations,
                                              'time_sleep': self.time_sleep,
                                              }, method='fetchone')[0]
        logger.info("Registered line task id {}".format(self.id))

        for job in self.jobs:
            job.line_task_id = self.id
            job.register()
            logger.info("Registered job id {}".format(job.id))

        return self

    def to_json(self):
        return dict(
            line_id=self.line_id,
            device_task_id=self.device_task_id,
            device_id=self.device_id,
            exec_time=self.exec_time,
            time=self.time,
            iterations=self.iterations,
            time_sleep=self.time_sleep,
            id=self.id,
        )

    serialize = to_json
