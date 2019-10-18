from flask import Blueprint

healthcheck = Blueprint("healthcheck", __name__)
@healthcheck.route("/", methods=["GET"])
# @jwt_required
def healthchecks():
    return "OK"