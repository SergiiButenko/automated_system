from datetime import datetime

from web.models.line_task import LineTask
from web.models.device import Device
from web.resources import Db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeviceTask:
    @staticmethod
    def get_by_id(device_task_id):
        q = """select dt.id, dt.device_id, dt.type, dt.exec_time, 
                json_agg(lt.*) as "line_tasks"
                from device_tasks as dt
                join line_tasks as lt
                on  dt.id = lt.device_task_id
                where lt.device_task_id = %(device_task_id)s
                group by dt.id
                      """
        device_task = Db.execute(query=q, params={'device_task_id': device_task_id}, method='fetchone')
        device_task['line_tasks'] = map(lambda x: LineTask(**x), device_task['line_tasks'])

        return DeviceTask(**device_task)

    @staticmethod
    def get_next_for_device_id(device_id):
        q = """SELECT dt.id, dt.device_id, dt.type, dt.exec_time, 
                json_agg(lt.*) as "line_tasks"
                FROM device_tasks as dt
                JOIN line_tasks as lt
                ON dt.id = lt.device_task_id
                WHERE dt.device_id = %(device_id)s
                AND lt.exec_time >= now() - INTERVAL '1 HOUR'
                GROUP BY dt.id
                LIMIT 1
        """
        device_task = Db.execute(query=q, params={'device_id': device_id}, method='fetchone')
        device_task['line_tasks'] = map(lambda x: LineTask(**x), device_task['line_tasks'])

        return DeviceTask(**device_task)

    @staticmethod
    def calculate(device_id, lines):
        exec_time = datetime.now()
        device = Device.get_by_id(device_id=device_id)

        line_tasks = list()
        for line_to_plan in lines:
            line = device.lines[line_to_plan['line_id']]
            task = LineTask(exec_time=exec_time,
                            device_id=device_id,
                            device_task_id=-1,
                            time=line_to_plan['time'],
                            iterations=line_to_plan['iterations'],
                            time_sleep=line_to_plan['time_sleep'],
                            relay_num=line.relay_num,
                            line_id=line_to_plan['line_id'],
                            )

            exec_time = task.next_rule_start_time
            line_tasks.append(task)

        return DeviceTask(device_id=device_id, line_tasks=line_tasks, exec_time=exec_time)

    def __init__(
        self,
        device_id,
        line_tasks,
        exec_time,
        id=-1,
        type='onetime',
    ):
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
        self.id = Db.execute(query=q, params={'device_id': self.device_id}, method='fetchone')[0]

        for line_task in self.line_tasks:
            line_task.device_task_id = self.id
            line_task.register()

        return self

    def to_json(self):
        return dict(
            id=self.id,
            device_id=self.device_id,
            line_tasks=self.line_tasks,
        )

    serialize = to_json
