import os, logging
from .device import Device

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class _Devices:
    def __init__(self):
        self.devices = dict()
        for _device in Device.get_all(console_id=os.environ["CONSOLE_ID"]):
            self.devices[_device.id] = _device
            _device.subscribe()
            logger.info("Listening to {} device_id".format(_device.id))

    def get_by_id(self, device_id):
        try:
            return self.devices[device_id]
        except Exception:
            logger.error("No {} device_id for console".format(device_id))
            return None

Devices = _Devices()