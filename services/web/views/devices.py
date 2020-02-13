from models import Device
from flask import jsonify, request, Blueprint

from flask_jwt_extended import get_jwt_identity, jwt_required

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

devices = Blueprint("devices", __name__)


@devices.route("/", methods=["GET"])
@jwt_required
def devices_lines_route():
    user_id = get_jwt_identity()
    devices = Device.get_by_user_id(user_id)
    
    return jsonify(devices=devices)


@devices.route("/<string:device_id>", methods=["GET"])
@jwt_required
def devices_lines_by_id_route(device_id):
    user_id = get_jwt_identity()
    device = Device.get_by_id(device_id, user_id)
    
    return jsonify(devices=[device])


@devices.route("/<string:device_id>/lines", methods=["GET"])
@jwt_required
def devices_by_id_lines_by_id_route(device_id):
    user_id = get_jwt_identity()
    device = Device.get_by_id(device_id, user_id)
    device.init_lines()

    return jsonify(devices=[device])
