from flask import Blueprint

healthcheck = Blueprint("healthcheck", __name__)
@healthcheck.route("/", methods=["GET"])
# @jwt_required
def healthcheck():
    return "OK"