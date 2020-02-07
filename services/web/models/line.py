from resources.lines_dao import LineDAO

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Line:
    @staticmethod
    def get_by_id(line_id):
        record = LineDAO.get_by_id(line_id)
        if record is None:
            raise Exception(f"No line_id '{line_id}' found")

        return Line(**record)

    @staticmethod
    def get_by_device_id(device_id):
        records = LineDAO.get_by_device_id(device_id)
        if len(records) == 0:
            raise Exception(f"No lines for '{device_id}' found")

        lines = [Line(**rec) for rec in records]
        lines.sort(key=lambda e: e.name)

        return lines

    def __init__(self, id, name, description, relay_num, settings, status):
        self.id = id
        self.name = name
        self.description = description
        self.settings = settings
        self.relay_num = relay_num
        self.status = status

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "settings": self.settings,
            "relay_num": self.relay_num,
            "status": self.status,
        }

    serialize = to_json
