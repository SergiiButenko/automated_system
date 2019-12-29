from celery import Celery
import os
import time
import json

CeleryApp = Celery(
    os.environ["CONSOLE_ID"],
    backend=os.environ["REDIS_BROKER"],
    broker=os.environ["REDIS_BROKER"],
)

if __name__ == "__main__":
    CeleryApp.start()
