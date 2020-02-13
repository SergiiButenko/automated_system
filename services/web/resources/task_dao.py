from providers import Db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskDAO():
    @staticmethod
    def get_by_id(line_id):
        q = """
            select
            l.*,
            jsonb_object_agg(setting, value) as settings
            from line_settings as s
            join lines as l on s.line_id = l.id
            where l.id = %(line_id)s
            group by l.id
        """
        return Db.execute(q, {"line_id": line_id}, method="fetchone")


    @staticmethod
    def get_by_device_id(device_id):
        q = """
            select
            l.*,
            jsonb_object_agg(setting, value) as settings
            from line_settings as s
            join lines as l on s.line_id = l.id
            where l.id in (
                select line_id from line_device where device_id = %(device_id)s
            ) 
            group by l.id
        """

        return Db.execute(q, {"device_id": device_id}, method="fetchall")
