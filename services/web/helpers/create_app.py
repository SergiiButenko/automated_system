from flask import Flask, request
from flask.json import JSONEncoder
from flask_jwt_extended import JWTManager, get_jwt_claims, verify_jwt_in_request
from flask_socketio import SocketIO

from werkzeug.exceptions import BadRequest

from web.resources import redis, Db

from web.models import *
from web.errors import *
from web.errors.errors_handler import handle_common_errors

import logging
import os
from functools import wraps
import eventlet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, (Device, Group, Line, User, LineTask, DeviceTask, Job)):
                return obj.serialize()
            iterable = iter(obj)
        except TypeError as e:
            logger.error(e)
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def create_flask_app(name):
    eventlet.monkey_patch()

    app = Flask(name)
    app.config.from_object("web.config")

    app.json_encoder = CustomJSONEncoder

    app = handle_common_errors(app)

    socketio = SocketIO(app, async_mode="eventlet", engineio_logger=False, message_queue=os.environ["REDIS_BROKER"])
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)

    return app, socketio


def create_jwt_app(app):
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        jti = decrypted_token["jti"]
        entry = redis.get(jti)
        if entry is None:
            return True
        return entry == "true"

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {"roles": user.roles}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.username

    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        current_user = User.find(user_identity=identity)
        if identity != current_user.username:
            return None

        return current_user

    @jwt.user_loader_error_loader
    def custom_user_loader_error(identity):
        raise WrongCreds()

    return jwt


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if "admin" not in claims["roles"]:
            raise UnexpectedRole()
        else:
            return fn(*args, **kwargs)

    return wrapper


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            if request.is_json is False:
                raise NoJson()

            request.json
        except BadRequest as e:
            raise JsonMalformed(message="Payload must be a valid json")
        return f(*args, **kw)

    return wrapper


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            # validate(request.json, current_app.config[schema_name])
            return f(*args, **kw)

        return wrapper

    return decorator
