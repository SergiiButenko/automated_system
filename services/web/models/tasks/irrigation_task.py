from datetime import datetime, timezone
from resources.task_dao import TaskDAO

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IrrigationTask:
    @staticmethod
    def get_by_id(task_id):
        device_task = TaskDAO.get_by_id(task_id)

        return IrrigationTask(**device_task)

    @staticmethod
    def get_next_for_device_id(device_id):
        device_task = TaskDAO.get_next_for_device_id(device_id)

        return IrrigationTask(**device_task)

    @staticmethod
    def calculate(device_id, lines):
        exec_time = datetime.now(timezone.utc)

        line_tasks = list()
        for line_to_plan in lines:
            task = LineTask(
                exec_time=exec_time,
                device_id=device_id,
                device_task_id=-1,
                time=line_to_plan["time"],
                iterations=line_to_plan["iterations"],
                time_sleep=line_to_plan["time_sleep"],
                line_id=line_to_plan["line_id"],
            )

            exec_time = task.next_rule_start_time
            line_tasks.append(task)

        return IrrigationTask(
            device_id=device_id, line_tasks=line_tasks, exec_time=exec_time
        )

    def __init__(self, device_id, line_tasks, exec_time, id=-1, type="onetime"):
        self.device_id = device_id
        self.line_tasks = line_tasks
        self.exec_time = exec_time
        self.id = id
        self.type = type

    def register(self):
        q = """
               INSERT INTO device_tasks(device_id)
               VALUES (%(device_id)s)
               RETURNING id
               """
        self.id = Db.execute(
            query=q, params={"device_id": self.device_id}, method="fetchone"
        )[0]

        for line_task in self.line_tasks:
            line_task.device_task_id = self.id
            line_task.register()

        return self

    def cancel(self):
        for line_task in self.line_tasks:
            line_task.cancel()
        
        pass

    def to_json(self):
        return dict(id=self.id, device_id=self.device_id, line_tasks=self.line_tasks)

    serialize = to_json
