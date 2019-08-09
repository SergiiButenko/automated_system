# An example
from flask import Blueprint
from flask import current_app as app

import bcrypt

import logging

from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
    get_jwt_identity,
    get_raw_jwt,
    jwt_refresh_token_required,
    jwt_required,
)

from web.errors import GeneralError, WrongCreds, UnableToRefresh
from web.models import User
from web.resources import Db, redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    logger.info(request.is_json)
    if not request.is_json:
        raise GeneralError(message="Empty JSON")

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        raise GeneralError(message="Empty password or username")

    current_user = User.find(user_identity=username)

    if current_user is None or bcrypt.hashpw(
        password.encode("utf-8"), current_user.password.encode("utf-8")
    ) != current_user.password.encode("utf-8"):
        logger.error("User's {} pass or email not correct".format(username))
        raise WrongCreds()

    logger.info("User {} logged in".format(current_user.username))

    access_token = create_access_token(identity=current_user)
    refresh_token = create_refresh_token(identity=current_user)

    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)

    redis.set(access_jti, "false", app.config["JWT_ACCESS_TOKEN_EXPIRES"] * 1.2)
    redis.set(refresh_jti, "false", app.config["JWT_REFRESH_TOKEN_EXPIRES"] * 1.2)

    ret = {"access_token": access_token, "refresh_token": refresh_token}

    return jsonify(ret), 201


@auth.route("/refreshToken", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    refresh_jti = get_raw_jwt()["jti"]
    status = redis.set(
        refresh_jti, "false", app.config["JWT_REFRESH_TOKEN_EXPIRES"] * 1.2
    )

    if status is False:
        raise UnableToRefresh()

    username = get_jwt_identity()
    current_user = User.find(user_identity=username)

    access_token = create_access_token(identity=current_user)
    access_jti = get_jti(encoded_token=access_token)

    redis.set(access_jti, "false", app.config["JWT_ACCESS_TOKEN_EXPIRES"] * 1.2)

    ret = {"access_token": access_token}

    return jsonify(ret), 200


# Endpoint for revoking the current users access token
@auth.route("/logout", methods=["DELETE"])
@jwt_required
def logout():
    jti = get_raw_jwt()["jti"]
    redis.set(jti, "true", app.config["JWT_ACCESS_TOKEN_EXPIRES"] * 1.2)

    return jsonify({"msg": "Access token revoked"}), 200
