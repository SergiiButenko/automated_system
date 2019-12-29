from models import Device
from flask import jsonify, request, Blueprint

from flask_jwt_extended import get_jwt_identity

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

devices = Blueprint("devices", __name__)


@devices.route("/", methods=["GET"])
# @jwt_required
def devices_lines_route():
    cr_user = get_jwt_identity()

    return jsonify(devices=Device.get_all(user_identity=cr_user))


@devices.route("/<string:device_id>", methods=["GET"])
# @jwt_required
def devices_lines_by_id_route(device_id):
    return jsonify(devices=[Device.get_by_id(device_id=device_id)])


@devices.route("/<string:device_id>/lines/<string:line_id>", methods=["PUT"])
# @jwt_required
def devices_by_id_lines_by_id_route(device_id, line_id):
    income_json = request.json

    device = Device.get_by_id(device_id=device_id)
    line_state = device.lines[line_id].state = income_json['desired_state']

    return jsonify(line_state=line_state)
