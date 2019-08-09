from web.models.line_task import LineTask
from web.resources import Db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Line:
    def __init__(self, id, name, description, relay_num, settings, state=-1):
        self.id = id
        self.name = name
        self.description = description
        self.settings = settings
        self.relay_num = relay_num
        self.state = state

        self.tasks = self._init_task()

    def _init_task(self):
        q = """
                    SELECT * from line_tasks
                    WHERE exec_time >= now() - INTERVAL '1 HOUR'
                    AND line_id = %(line_id)s
                    ORDER BY exec_time ASC
                    LIMIT 1
                    """

        record = Db.execute(query=q, params={"line_id": self.id}, method='fetchone')

        tasks = list()
        if record is None:
            return tasks

        tasks.append(LineTask(**record))
        tasks.sort(key=lambda e: e.exec_time)

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
            "state": self.state,
            "tasks": self.tasks,
        }

    serialize = to_json
