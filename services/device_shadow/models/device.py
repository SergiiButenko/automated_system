# This is an example of a complex object that we could build
# a JWT from. In practice, this will likely be something
# like a SQLAlchemy instance.
import logging
import json
import Redis

from resources import Db, Mosquitto
from .line import Line

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Device:
    @staticmethod
    def get_all(console_id):
        q = """
            select
            d.*,
            jsonb_object_agg(setting, value) as settings
            from device_settings as s
            join devices as d on s.device_id = d.id
            where d.console = %(console)s
            group by d.id
            """

        records = Db.execute(q, {"console": console_id}, method="fetchall")
        devices = list()

        if len(records) == 0:
            logger.info("No devices for console '{}' found".format(console_id))
            return devices

        for rec in records:
            devices.append(Device(**rec))

        devices.sort(key=lambda e: e.name)

        return devices
    
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
        """.format(
            line=line
        )

        return Db.execute(query=q, params={"device_id": device_id}, method="fetchall")

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
        self.state = None
        self.lines = self._init_lines()
        self.mosquitto_topic = self.id + '/device'

    def _init_lines(self):
        records = Device._get_device_lines(device_id=self.id, line_id=None)

        lines = dict()
        for rec in records:
            logger.info(rec["id"])
            lines[rec["id"]] = Line(device_id=self.id, **rec)

        return lines

    def save_remote_state(self):
        msg = dict(action="set_state", device_id=self.id, state=self.lines)
        logger.info("sending message, topic: {}; message: {}".format(self.id, msg))
        Mosquitto.send_message(topic=self.mosquitto_topic, payload=msg)

    def refresh_lines_state(self):
        msg = dict(action="get_state", device_id=self.id)

        logger.info("sending message, topic: {}; message: {}".format(self.id, msg))
        Mosquitto.send_message(topic=self.mosquitto_topic, payload=msg)

    def set_line_state_by_relay_num(self, relay_num, state):
        for _line in self.lines:
            if _line.relay_num == relay_num:
                _line.relay_num.state = state
                logger.info("{} line state is now {}".format(_line.id, _line.state))
                return _line.state
        
        return None

    def set_line_state_by_id(self, line_id, state):
        self.lines[line_id].state = state
        return self.get_line_state_by_id(line_id)

    def get_line_state_by_id(self, line_id):
        self.refresh_lines_state()
        return self.lines[line_id].state
 
    def subscribe(self):
        Mosquitto.subscribe(self.id)
        logger.info("Listening to {} device_id".format(self.id))

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
            "state": self.state,
            "lines": self.lines,
        }

    serialize = to_json
