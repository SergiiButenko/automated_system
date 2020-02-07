from models import line
from flask import jsonify, request, Blueprint

from flask_jwt_extended import get_jwt_identity

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

lines = Blueprint("lines", __name__)

@lines.route("/<string:line_id>", methods=["GET"])
@jwt_required
def devices_line_by_id_route(line_id):
    line = Line.get_by_id(line_id)
    
    return jsonify(lines=[line])