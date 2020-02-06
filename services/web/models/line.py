from models.line_task import LineTask
from resources import Db, CeleryApp

import logging, requests, os, time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Line:
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
