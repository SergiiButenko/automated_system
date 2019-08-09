import logging
import os
from flask import Flask, request

from models import Device

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEVICES = {device.id: device for device in Device.get_all(console_id=os.environ["CONSOLE_ID"])}
for _device_id, _device in DEVICES.items():
    logger.info("Listening to {} device_id".format(_device_id))
    _device.listen()

app = Flask(__name__)


@app.route("/<string:device_id>", methods=["GET"])
def get_state(device_id):
    return DEVICES[device_id].state


@app.route("/<string:device_id>", methods=["POST"])
def post_state(device_id):
    data = request.get_json

    DEVICES[device_id].state = data

    return device_id


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
