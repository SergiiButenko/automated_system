import logging
import os
from flask import Flask, request, jsonify
from flask.json import JSONEncoder

from models import Device, Line

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEVICES = {
    device.id: device for device in Device.get_all(console_id=os.environ["CONSOLE_ID"])
}
for _device_id, _device in DEVICES.items():
    _device.subscribe()
    logger.info("Listening to {} device_id".format(_device_id))


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, (Device, Line)):                
                return obj.serialize()
            iterable = iter(obj)
        except TypeError as e:
            logger.error(e)
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder


@app.route("/<string:device_id>/lines", methods=["GET"])
def get_state(device_id):
    return jsonify(lines=DEVICES[device_id].lines)

@app.route("/<string:device_id>/lines/<string:line_id>", methods=["GET"])
def get_line_state(device_id, line_id):
    return jsonify(lines=DEVICES[device_id].lines[line_id])


@app.route("/<string:device_id>/lines/<string:line_id>", methods=["PUT"])
def post_state(device_id, line_id):
    data = request.get_json()
    
    logger.info("current state {}".format(DEVICES[device_id].lines[line_id].state))
    DEVICES[device_id].lines[line_id].state = data['state']
    logger.info("new state {}".format(DEVICES[device_id].lines[line_id].state))

    return jsonify(state=DEVICES[device_id].lines[line_id])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
