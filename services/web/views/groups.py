from web.models import Group
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
    cr_user = get_jwt_identity()

    return jsonify(groups=Group.get_all(user_identity=cr_user))


@groups.route("/<string:group_id>", methods=["GET"])
@jwt_required
def groups_lines_route(group_id):
    return jsonify(groups=[Group.get_by_id(group_id=group_id)])
