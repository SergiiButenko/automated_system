from web.resources import Db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Job:
    def __init__(self, line_task_id, line_id, device_id, desired_device_state, exec_time, state="", id=-1):
        self.id = id
        self.line_task_id = line_task_id
        self.line_id = line_id
        self.device_id = device_id
        self.desired_device_state = desired_device_state
        self.exec_time = exec_time
        self.state = state

    def register(self):
        q = """
                    INSERT INTO jobs_queue
                    (line_task_id, line_id, device_id, desired_device_state, exec_time)
                    VALUES (%(line_task_id)s, %(line_id)s, %(device_id)s, %(desired_device_state)s, %(exec_time)s)
                    RETURNING id
                    """
        self.id = Db.execute(query=q, params=self.to_json(), method='fetchone')[0]

        return self

    def to_json(self):
        return dict(
            id=self.id,
            line_task_id=self.line_task_id,
            line_id=self.line_id,
            device_id=self.device_id,
            desired_device_state=self.desired_device_state,
            exec_time=self.exec_time,
            state=self.state,
        )

    serialize = to_json
