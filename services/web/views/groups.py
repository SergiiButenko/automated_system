from models import Group
from flask import Blueprint
from flask import jsonify

from flask_jwt_extended import get_jwt_identity, jwt_required

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
groups = Blueprint("groups", __name__)


@groups.route("/", methods=["GET"])
@jwt_required
def groups_route():
    user_id = get_jwt_identity()
    groups = Group.get_by_user_id(user_id)
    
    return jsonify(groups=groups)


@groups.route("/<string:group_id>", methods=["GET"])
@jwt_required
def groups_id_route(group_id):
    user_id = get_jwt_identity()
    group = Group.get_by_id(group_id, user_id)
    
    return jsonify(groups=[group])

@groups.route("/<string:group_id>/devices", methods=["GET"])
@jwt_required
def groups_id_device_route(group_id):
    user_id = get_jwt_identity()
    group = Group.get_by_id(group_id, user_id)
    group.init_devices()

    return jsonify(groups=[group])
