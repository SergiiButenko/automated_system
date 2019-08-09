from web.errors import COMMON_ERROR

from werkzeug.exceptions import HTTPException
from flask_jwt_extended.exceptions import JWTExtendedException
from web.errors import GeneralError

from flask import jsonify
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def error_obj(message, code, description):
    tmp = dict(message=message, code=code, description=str(description))
    return jsonify(tmp), tmp["code"]


def handle_error(error):
    def_code = 500
    def_message = "Unexpected error"

    if isinstance(error, GeneralError):
        return error_obj(message=error.message, code=error.code, description=error)

    if isinstance(error, HTTPException):
        return error_obj(message=error.description, code=error.code, description=error)

    if isinstance(error, JWTExtendedException):
        return error_obj(message=error.msg, code=error.code, description=error)

    return error_obj(message=def_message, code=def_code, description=error)


def handle_common_errors(app):
    for clazz in COMMON_ERROR:
        app.register_error_handler(clazz, handle_error)

    return app
