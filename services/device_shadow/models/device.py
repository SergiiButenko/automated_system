# This is an example of a complex object that we could build
# a JWT from. In practice, this will likely be something
# like a SQLAlchemy instance.
import logging

from resources import Db, Mosquitto


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

        records = Db.execute(q, {'console': console_id}, method='fetchall')
        devices = list()

        if len(records) == 0:
            logger.info("No devices for console '{}' found".format(console_id))
            return devices

        for rec in records:
            devices.append(Device(**rec))

        devices.sort(key=lambda e: e.name)

        return devices

    @staticmethod
    def _on_connect(userdata, flags, rc):
        logger.info("Connected With Result Code {}".format(rc))

    @staticmethod
    def _on_disconnect(userdata, rc):
        logger.info("Disconnected From Broker")

    @staticmethod
    def _on_message(userdata, message):
        logger.info(message.payload.decode())
        logger.info(message.topic)

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

        self.__state = None
        self.mqtt = Mosquitto(
            on_message=Device._on_message,
            on_connect=Device._on_connect,
            on_disconnect=Device._on_disconnect,
            topic=id
        )

    @property
    def state(self):
        self.request_state()
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state
        # send request to websocket

    def request_state(self):
        return self.mqtt.send_message(topic="{}/state".format(self.id), payload=dict(action='get_state'))

    def listen(self):
        self.mqtt.listen()

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
        }

    serialize = to_json
