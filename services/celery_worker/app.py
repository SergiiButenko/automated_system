from celery import Celery
import os
import time
import json

CeleryApp = Celery(
    os.environ["CONSOLE_ID"],
    backend=os.environ["REDIS_BROKER"],
    broker=os.environ["REDIS_BROKER"],
    # include=[
    #     "get_device_status",
    # ],
)


@CeleryApp.task
def get_device_status(device_id):
    print("get_device_status task begins")
    # sleep 5 seconds
    time.sleep(5)
    print("long time task finished")
    return json.dumps({"test": device_id})


if __name__ == '__main__':
    CeleryApp.start()
