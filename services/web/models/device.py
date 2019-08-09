# This is an example of a complex object that we could build
# a JWT from. In practice, this will likely be something
# like a SQLAlchemy instance.
import logging

from web.models.line import Line
from web.resources import Db

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

        records = Db.execute(q, {'user_identity': user_identity}, method='fetchall')
        devices = list()

        if len(records) == 0:
            logger.info("No devices for user '{}' found".format(user_identity))
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

        self.lines = self._init_lines()
        self.state = self.refresh_state()

    def _init_lines(self):
        records = Device._get_device_lines(device_id=self.id, line_id=None)

        lines = dict()
        for rec in records:
            lines[rec['id']] = Line(**rec)

        return lines

    def refresh_state(self):
        if self.lines is None:
            self.lines = self._init_lines()

        # get from redis
        # request change
        state = "offline"
        if self.settings["comm_protocol"] == "network":
            try:
                # lines_state = requests.get(url=self.settings["ip"] + "99")
                # lines_state.raise_for_status()

                # lines_state = re.findall("\d+", lines_state.text)
                # logger.info(lines_state)

                # lines_state = list(map(int, lines_state))
                # logger.info(lines_state)
                lines_state = [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1]
                state = "online"

                for line in self.lines:
                    line.state = lines_state[line.relay_num]
            except Exception as e:
                logger.error("device is offline")
                logger.error(e)
                state = "offline"

        return state

    def set_state(self, desired_state):
        # get from redis
        # request change
        state = self.state
        if self.settings["comm_protocol"] == "network":
            try:
                # lines_state = requests.get(url=self.settings["ip"] + "99")
                # lines_state.raise_for_status()

                # lines_state = re.findall("\d+", lines_state.text)
                # logger.info(lines_state)

                # lines_state = list(map(int, lines_state))
                # logger.info(lines_state)
                lines_state = [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1]
                state = "online"

                for line in self.lines:
                    line.state = lines_state[line.relay_num]
            except Exception as e:
                logger.error("device is offline")
                logger.error(e)
                state = "offline"

        self.state = state

        return self

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
