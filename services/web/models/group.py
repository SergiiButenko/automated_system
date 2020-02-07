# This is an example of a complex object that we could build
# a JWT from. In practice, this will likely be something
# like a SQLAlchemy instance.
from resources.group_dao import GroupDAO
from models import Device

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Group:
    @staticmethod
    def get_by_id(group_id, user_id):
        group = GroupDAO.get_by_id(group_id, user_id)
        if group is None:
            raise Exception(f"No group_id {group_id} found")

        return Group(**group)

    @staticmethod
    def get_by_user_id(user_id):
        records = GroupDAO.get_by_user_id(user_id)
        if len(records) == 0:
            raise Exception(f"No groups for user '{user_id}' found")

        groups = [Group(**rec) for rec in records]
        groups.sort(key=lambda e: e.name)

        return groups

    def __init__(self, id, name, description, devices=[]):
        self.id = id
        self.name = name
        self.description = description
        self.devices = []

    def init_devices(self):
        return Device.get_by_group_id(self.id)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "devices": self.devices,
        }

    serialize = to_json
