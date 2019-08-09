# This is an example of a complex object that we could build
# a JWT from. In practice, this will likely be something
# like a SQLAlchemy instance.
from web.models import Device
from web.resources import Db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Group:
    @staticmethod
    def get_by_id(group_id):
        q = """
                       select * from groups where id = %(group_id)s
                        """

        group = Db.execute(q, params={'group_id': group_id}, method="fetchone")
        if group is None:
            raise Exception("No group_id {} found".format(group_id))

        group = Group(**group)
        group.init_devices()

        return group

    @staticmethod
    def get_all(user_identity):
        q = """
                       select g.* from groups as g where id in (
                            select group_id from device_groups where device_id in (
                                select device_id from device_user where user_id in (
                                                select id from users where name = %(user_identity)s
                                            )
                            )
                        )
                        """

        records = Db.execute(q, params={'user_identity': "admin"}, method="fetchall")
        groups = list()

        if len(records) == 0:
            logger.info("No groups for user '{}' found".format(user_identity))
            return groups

        for rec in records:
            groups.append(Group(**rec))

        groups.sort(key=lambda e: e.name)

        return groups

    def __init__(self, id, name, description, devices=[]):
        self.id = id
        self.name = name
        self.description = description
        self.devices = []

    def init_devices(self):
        q = """
                    select
                    d.*,
                    jsonb_object_agg(setting, value) as settings
                    from device_settings as s
                    join devices as d on s.device_id = d.id
                    where s.device_id in (
                    select id from devices where id in (
                        select device_id from device_groups where group_id = %(group_id)s
                        )
                    )
                    group by d.id
                    """
        records = Db.execute(q, {'group_id': self.id}, method='fetchall')
        if len(records) == 0:
            logger.info("No devices in group_id '{}'".format(self.id))
            return self

        for rec in records:
            device = Device(**rec)
            self.devices.append(device)

        self.devices.sort(key=lambda e: e.name)

        return self

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "devices": self.devices,
        }

    serialize = to_json
