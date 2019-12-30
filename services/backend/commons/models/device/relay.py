from commons.models.device.base_device import BaseDevice
from commons.models.line import Line
from commons.providers.logger import Logger

logger = Logger.get_logger(__name__)

class Relay(BaseDevice):

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        self.lines = None
    
    def _init_lines(self):
        records = BaseDevice._get_device_lines(device_id=self.id, line_id=None)

        lines = dict()
        for rec in records:
            lines[rec["id"]] = Line(device_id=self.id, **rec)

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