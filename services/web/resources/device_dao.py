from providers import Db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeviceDAO():
    @staticmethod
    def get_by_id(device_id, user_id):
        q = """
            select
            d.*,
            jsonb_object_agg(setting, value) as settings
            from device_settings as s
            join devices as d on s.device_id = d.id
            where s.device_id = %(device_id)s
            and s.user_id = %(user_id)s
            group by d.id
            """

        return Db.execute(q, {"device_id": device_id, "user_id": user_id}, method="fetchone")


    @staticmethod
    def get_by_user_id(user_id):
        q = """
            select
            d.*,
            jsonb_object_agg(setting, value) as settings
            from device_settings as s
            join devices as d on s.device_id = d.id
            where d.user_id = %(user_id)s
            group by d.id
            """

        return Db.execute(q, {"user_id": user_id}, method="fetchall")

    @staticmethod
    def get_by_group_id(group_id):
        q = """
            select
            d.*,
            jsonb_object_agg(setting, value) as settings
            from device_settings as s
            join devices as d on s.device_id = d.id
            where s.device_id in (
                select device_id from device_groups where group_id = %(group_id)s
                )
            group by d.id
            """
        return Db.execute(q, {"group_id": group_id}, method="fetchall")
        