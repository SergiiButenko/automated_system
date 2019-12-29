import json, logging
from datetime import datetime, timezone
from models import Device

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MsgAnalyzer:
    allowed_statuses = ["pending", "failed"]
    allowed_delta = 10

    @staticmethod
    def strptime(time_str):
        time_str = time_str[:19]
        dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return dt

    def __init__(
        self,
        id,
        line_task_id,
        line_id,
        device_id,
        desired_state,
        exec_time,
        expire_time,
        status,
    ):
        self.line_task_id = line_task_id
        self.line_id = line_id
        self.device_id = device_id
        self.desired_state = desired_state
        # self.exec_time = MsgAnalyzer.strptime(exec_time)
        self.exec_time = exec_time
        self.expire_time = expire_time
        self.status = status

    def _update(self):
        pass

    def _exec(self):
        device = Device.get_by_id(self.device_id)
        device.lines[self.line_id].state = self.desired_state

    def analyze_conditions(self, force=False):
        if self.status in MsgAnalyzer.allowed_statuses:
            return True

        return False

    def analyze_time(self):
        now = datetime.now(timezone.utc)
        logger.info(type(self.expire_time))
        logger.info(type(now))
        logger.info(self.expire_time > now)

        return True

    def analyze(self):
        return self.analyze_conditions() and self.analyze_time()

    def analyze_and_exec(self, force=False):
        if force is True:
            logger.info("Force sending message")
            self._exec()

        if self.analyze() is True:
            logger.info("Applied rules allow execution")
            self._exec()

            return True
        else:
            logger.info("Applied rules deny execution")
            return False
