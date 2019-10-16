import logging, os, requests
from resources import Mosquitto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Line:
    def __init__(self, id, device_id, name, description, relay_num, settings):
        self.id = id
        self.device_id = device_id
        self.name = name
        self.description = description
        self.settings = settings
        self.relay_num = relay_num

        self.__state = None

    @property
    def state(self):
        self.request_state()
        return self.__state

    @state.setter
    def state(self, state):
        msg = dict(action="set_state", device_id=self.device_id, state=state)

        self.__state = state['state']

        logger.info("sending message, topic: {}; message: {}".format(self.id, msg))
        Mosquitto.send_message(topic=self.device_id, payload=msg)
        # send request to websocket

    def request_state(self):
        msg = dict(action="get_state", device_id=self.device_id)

        logger.info("sending message, topic: {}; message: {}".format(self.id, msg))
        Mosquitto.send_message(topic=self.device_id, payload=msg)

    def to_json(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "name": self.name,
            "description": self.description,
            "settings": self.settings,
            "relay_num": self.relay_num,
            "state": self.__state,
        }

    serialize = to_json
