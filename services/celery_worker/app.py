from celery import Celery
import os
import time
import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CeleryApp = Celery(
    os.environ["CONSOLE_ID"],
    backend=os.environ["REDIS_BROKER"],
    broker=os.environ["REDIS_BROKER"],
)
CeleryApp.conf.task_serializer = 'json'


@CeleryApp.task(name='get_line_state')
def get_line_state(device_id, line_id):
    logger.info("Sending get status: to device_id '{}'".format(device_id))
    url = "http://" + os.environ["DEVICE_SHADOW_HOST"] + '/' + device_id + "/lines/" + line_id
    r = requests.get(url=url)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    CeleryApp.start()

