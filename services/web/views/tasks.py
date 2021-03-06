from models.tasks.task_factory import TaskFactory
from flask import jsonify, request, Blueprint

from flask_jwt_extended import get_jwt_identity, jwt_required

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tasks = Blueprint("tasks", __name__)


@tasks.route("/<string:task_type>", methods=["POST"])
@jwt_required
def set_rules_for_device(task_type):
    income_json = request.json
    device_id = income_json.get('device_id')
    lines = income_json.get('lines')

    Task = TaskFactory.get_serializer(task_type)

    device_task = Task.calculate(device_id, lines)
    device_task.register()

    return jsonify(tasks=device_task)


@tasks.route("/<string:task_id>", methods=["DELETE"])
# @jwt_required
def delete_rules_for_device(device_id):
    income_json = request.json

    device_task = DeviceTask.get_by_id(device_task_id=income_json["lines"])
    device_task = device_task.cancel()

    return "OK"


@tasks.route("/<string:date_start>/<string:date_end>", methods=["GET"])
# @jwt_required
def get_all_tasks(date_start, date_end):
    cr_user = get_jwt_identity()
    return "OK"


@tasks.route(
    "/<string:date_start>/<string:date_end>", methods=["GET"]
)
@jwt_required
def get_rules_for_device(device_id):
    cr_user = get_jwt_identity()

    # to check device exists
    Device.get_by_id(device_id=device_id, user_identity=cr_user)

    tasks = DeviceTask.get_next_task_by_device_id(device_id=device_id)

    return jsonify(tasks=tasks)
