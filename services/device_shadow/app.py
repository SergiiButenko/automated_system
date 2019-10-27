import logging
import os
from flask import Flask, request, jsonify
from flask.json import JSONEncoder

from models import Device, Line
from resources import Devices

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
    device = Devices.get_by_id(device_id)

    return jsonify(lines=device.lines)

@app.route("/<string:device_id>/lines/<string:line_id>", methods=["GET"])
def get_line_state(device_id, line_id):
    device = Devices.get_by_id(device_id)
    
    return jsonify(lines=device.get_line_by_id(line_id))

@app.route("/<string:device_id>/lines/<string:line_id>", methods=["PUT"])
def post_state(device_id, line_id):
    data = request.get_json()
    device = Devices.get_by_id(device_id)

    logger.info("current state {}".format(device.get_line_state_by_id(line_id)))
    device.set_line_state_by_id(line_id, data['state'])
    
    logger.info("new state {}".format(device.get_line_state_by_id(line_id)))

    return jsonify(lines=device.get_line_by_id(line_id))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
