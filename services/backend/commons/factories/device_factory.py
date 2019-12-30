class DeviceFactory():
    @staticmethod
    def get_by_id(device_id):
        q = """
                    select
                    d.*,
                    jsonb_object_agg(setting, value) as settings
                    from device_settings as s
                    join devices as d on s.device_id = d.id
                    where s.device_id = %(device_id)s
                    group by d.id
                    """

        device = Db.execute(q, {"device_id": device_id}, method="fetchone")
        if device is None:
            raise Exception("No device_id '{}' found".format(device_id))

        return Device(**device)

    @staticmethod
    def get_all(user_identity):
        q = """
                    select
                    d.*,
                    jsonb_object_agg(setting, value) as settings
                    from device_settings as s
                    join devices as d on s.device_id = d.id
                    where s.device_id in (
                    select id from devices where id in (
                        select device_id from device_user where user_id in (
                            select id from users where name = %(user_identity)s
                            )
                        )
                    )
                    group by d.id
                    """

        records = Db.execute(q, {"user_identity": user_identity}, method="fetchall")
        devices = list()

        if len(records) == 0:
            logger.info("No devices for user '{}' found".format(user_identity))
            return devices

        for rec in records:
            devices.append(Device(**rec))

        devices.sort(key=lambda e: e.name)

        return devices


import logging

from models.line import Line
from resources import Db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

 

   