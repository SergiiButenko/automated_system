import logging, os, requests
from resources import Mosquitto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Line:
    def __init__(self, id, device_id, name, description, relay_num, settings, status):
        self.id = id
        self.device_id = device_id
        self.name = name
        self.description = description
        self.settings = settings
        self.relay_num = relay_num
        self.status = status

        self.__state = dict(current=None, desired=None, updated=None)

    @property
    def state(self):
        self.request_state()
        return self.__state

    @state.setter
    def state(self, state):
        self.__state['desired'] = state

    def save_remote_state(self):
        new_state = dict(relay_num=self.relay_num, desire_state=self.state['desired'])
        msg = dict(action="set_state", device_id=self.device_id, state=new_state)

        logger.info("sending message, topic: {}; message: {}".format(self.id, msg))
        Mosquitto.send_message(topic=self.device_id+'/device', payload=msg)

    def request_state(self):
        msg = dict(action="get_state", device_id=self.device_id)

        logger.info("sending message, topic: {}; message: {}".format(self.id, msg))
        Mosquitto.send_message(topic=self.device_id+'/device', payload=msg)

    def to_json(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "name": self.name,
            "description": self.description,
            "settings": self.settings,
            "relay_num": self.relay_num,
            "state": self.__state,
            "status": self.status,
        }

    serialize = to_json
