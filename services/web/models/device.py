import logging

from models.line import Line
from resources.device_dao import DeviceDAO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Device:
    @staticmethod
    def get_by_id(device_id, user_id):
        record = DeviceDAO.get_by_id(device_id, user_id)
        if record is None:
            raise Exception(f"No device_id '{device_id}' found")

        return Device(**record)

    @staticmethod
    def get_by_user_id(user_id):
        records = DeviceDAO.get_by_user_id(user_id)
        if len(records) == 0:
            raise Exception(f"No devices for user '{user_id}' found")

        devices = [Device(**rec) for rec in records]
        devices.sort(key=lambda e: e.name)

        return devices

    @staticmethod
    def get_by_group_id(group_id):
        records = DeviceDAO.get_by_group_id(group_id)
        if len(records) == 0:
            raise Exception(f"No devices in group_id '{group_id}'")

        devices = [Device(**rec) for rec in records]
        devices.sort(key=lambda e: e.name)

        return devices

    def __init__(
        self,
        id,
        name,
        description,
        type,
        device_type,
        protocol,
        settings,
        state,
        updated_at=None,
        console=None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.device_type = device_type
        self.protocol = protocol
        self.settings = settings
        self.console = console
        self.state = state
        self.updated_at = updated_at

        self.lines = []

    def init_lines(self):
        return Line.get_by_device_id(self.id)
        
    def refresh_state(self):
        pass

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "device_type": self.device_type,
            "protocol": self.protocol,
            "settings": self.settings,
            "lines": self.lines,
            "state": self.state,
            "updated_at": self.updated_at,
        }

    serialize = to_json
