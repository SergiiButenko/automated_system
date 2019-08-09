# This is an example of a complex object that we could build
# a JWT from. In practice, this will likely be something
# like a SQLAlchemy instance.
import logging
import os
import time

from localworker.models.line import Line
from localworker.resources import Db, MQTT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Device:
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

        device = Db.execute(q, {'device_id': device_id}, method='fetchone')
        if device is None:
            raise Exception("No device_id '{}' found".format(device_id))

        return Device(**device)

    @staticmethod
    def _get_device_lines(device_id, line_id):
        line = ""
        if line_id is not None:
            line = " and line_id = '{line_id}'".format(line_id=line_id)

        q = """
            select
            l.*,
            jsonb_object_agg(setting, value) as settings
            from line_settings as s
            join lines as l on s.line_id = l.id
            where l.id in (
                select line_id from line_device where device_id = %(device_id)s
            ) {line}
            group by l.id
        """.format(line=line)

        return Db.execute(query=q, params={'device_id': device_id}, method='fetchall')

    def __init__(
        self,
        id,
        name,
        description,
        type,
        device_type,
        model,
        version,
        settings,
        console=None,
        lines=None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.device_type = device_type
        self.model = model
        self.version = version
        self.settings = settings
        self.console = console

        self.__lines = None
        self.__state = None

    @property
    def lines(self):
        if self.__lines is not None:
            return self.__lines

        records = Device._get_device_lines(device_id=self.id, line_id=None)

        lines = dict()
        for rec in records:
            lines[rec['id']] = Line(**rec)
        self.__lines = lines

        return self.__lines

    @property
    def state(self):
        if self.__state is not None:
            return self.__state

        if self.settings["comm_protocol"] == "radio":
            pass
        elif self.settings["comm_protocol"] == "network":
            logger.info("Sending get status: to device_id '{}'".format(self.id))
            return True

    @state.setter
    def state(self, desired_state):
        if self.settings["comm_protocol"] == "radio":
            pass
        elif self.settings["comm_protocol"] == "network":
            logger.info("Sending new status: '{}' to device_id '{}'".format(desired_state, self.id))
            return True

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "device_type": self.device_type,
            "model": self.model,
            "version": self.version,
            "settings": self.settings,
            "lines": self.lines,
            "state": self.state,
        }

    serialize = to_json
