from web.models import Device
from flask import jsonify, Blueprint

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
def devices_lines_by_id_route(device_id=None):
    return jsonify(devices=[Device.get_by_id(device_id=device_id)])
