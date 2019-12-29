from models.line_task import LineTask
from resources import Db, CeleryApp

import logging, requests, os, time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Line:
    def __init__(self, id, name, description, relay_num, settings, status, device_id):
        self.id = id
        self.device_id = device_id
        self.name = name
        self.description = description
        self.settings = settings
        self.relay_num = relay_num
        self.status = status
        self.__state = None

        self.tasks = self._init_task()

    @property
    def state(self):
        # if self.settings["comm_protocol"] == "radio":
        #     pass
        # elif self.settings["comm_protocol"] == "network":
        r = CeleryApp.signature('get_line_state', kwargs={'device_id': self.device_id,'line_id': self.id}).delay()
        while r.status != "SUCCESS":
            time.sleep(0.1)
        
        self.__state = r.result['lines']['state']

        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    def _init_task(self):
        q = """
                    SELECT * from line_tasks
                    WHERE expire_time >= now()
                    AND line_id = %(line_id)s
                    ORDER BY exec_time ASC
                    LIMIT 1
                    """

        record = Db.execute(query=q, params={"line_id": self.id}, method="fetchone")

        tasks = list()
        if record is None:
            return tasks

        tasks.append(LineTask(**record))
        tasks.sort(key=lambda e: e.expire_time)

        return tasks

    def register_task(self, task):
        prev_tasks = self.tasks

        task.register()
        self.tasks = self._init_task()

        if prev_tasks != self.tasks:
            logger.info("Should send websocket notify")

        return self

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "settings": self.settings,
            "relay_num": self.relay_num,
            "status": self.status,
            "state": self.state,
            "tasks": self.tasks,
        }

    serialize = to_json
