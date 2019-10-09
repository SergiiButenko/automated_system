import logging
import os
from flask import Flask, request

from models import Device

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEVICES = {
    device.id: device for device in Device.get_all(console_id=os.environ["CONSOLE_ID"])
}
for _device_id, _device in DEVICES.items():
    _device.subscribe()
    logger.info("Listening to {} device_id".format(_device_id))

app = Flask(__name__)


@app.route("/<string:device_id>", methods=["GET"])
def get_state(device_id):
    return DEVICES[device_id].state


@app.route("/<string:device_id>", methods=["POST"])
def post_state(device_id):
    data = request.get_json()

    logger.info("received json {}".format(data))
    logger.info("current state {}".format(DEVICES[device_id].state))

    DEVICES[device_id].state = data

    logger.info("new state {}".format(DEVICES[device_id].state))

    return device_id


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
