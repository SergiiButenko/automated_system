import logging
import os
from flask import Flask, request, jsonify
from flask.json import JSONEncoder

from models import Device, Line

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    return jsonify(lines=Device.get_from_cache(device_id).lines)

@app.route("/<string:device_id>/lines/<string:line_id>", methods=["GET"])
def get_line_state(device_id, line_id):
    return jsonify(lines=Device.get_from_cache(device_id).lines[line_id])


@app.route("/<string:device_id>/lines/<string:line_id>", methods=["PUT"])
def post_state(device_id, line_id):
    data = request.get_json()
    _device = Device.get_from_cache(device_id)

    logger.info("current state {}".format(_device.lines[line_id].state))
    _device.lines[line_id].state = data['state']
    _device.lines[line_id].save_remote_state()
    _device.save_to_cache()

    logger.info("new state {}".format(_device.lines[line_id].state))

    return jsonify(state=_device.lines[line_id])


for _device in Device.get_all(console_id=os.environ["CONSOLE_ID"]):
    _device.subscribe()
    _device.save_to_cache()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
