from providers import Db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LineDAO():
    @staticmethod
    def get_by_id(task_id):
        q = """"""
        return Db.execute(
            query=q, params={"task_id": task_id}, method="fetchone"
        )

    @staticmethod
    def get_next_for_device_id(device_id):
        q = """"""
        return Db.execute(
            query=q, params={"device_id": device_id}, method="fetchone"
        )
