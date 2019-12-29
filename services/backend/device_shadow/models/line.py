import logging

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

        self.__state = dict(current=None, desired=None, updated=None)

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state['desired'] = state

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "settings": self.settings,
            "relay_num": self.relay_num,
            "state": self.__state,
            "status": self.status,
        }

    serialize = to_json
