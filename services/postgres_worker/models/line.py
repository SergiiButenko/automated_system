import logging, os, requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Line:
    def __init__(self, id, device_id, name, description, relay_num, settings, status):
        self.id = id
        self.device_id = device_id
        self.status = status
        self.name = name
        self.description = description
        self.settings = settings
        self.relay_num = relay_num

        self.__state = None

    @property
    def state(self):
        if self.__state is not None:
            return self.__state

        # if self.settings["comm_protocol"] == "radio":
        #     pass
        # elif self.settings["comm_protocol"] == "network":
        logger.info("Sending get status: to device_id '{}'".format(self.id))
        url = "http://" + os.environ["DEVICE_SHADOW_HOST"] + '/' + self.device_id + "/lines/" + self.id
        r = requests.get(url=url)
        r.raise_for_status()
        self.__state = r.to_json()['lines']['state']

        return self.__state

    @state.setter
    def state(self, desired_state):
        # if self.settings["comm_protocol"] == "radio":
        #     pass
        # elif self.settings["comm_protocol"] == "network":
        logger.info(
            "Sending new status: '{}' to device_id '{}'".format(
                desired_state, self.id
            )
        )
        url = "http://" + os.environ["DEVICE_SHADOW_HOST"] + '/' + self.device_id + "/lines/" + self.id
        r = requests.put(url=url, json=dict(state=desired_state))
        r.raise_for_status()

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
