import json
import logging
import os
import threading
import schedule
import time

from datetime import datetime

from resources.db import Db

# from helpers.messages import send_message
from models import MsgAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scheduler():
    logger.info("GET ACTIVE JOBS")
    get_active_jobs = """
                    SELECT id, line_task_id, line_id, device_id, desired_state, exec_time, expire_time, status
                    FROM (
                    SELECT
                        ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY expire_time desc) AS r,
                        t.*
                    FROM
                        jobs_queue t) jobs
                    WHERE
                    jobs.r <= 1 and jobs.expire_time >= (now() at time zone 'utc') and status = 'pending';"""

    messages = Db.execute(query=get_active_jobs, method="fetchall")
    logger.info("GOT ACTIVE JOBS")

    for _message in messages:
        logger.info(_message)
        msg = MsgAnalyzer(**_message)
        msg.analyze_and_exec()


def scheduler_super_task():
    schedule.every().minute.do(scheduler)
    while True:
        schedule.run_pending()
        time.sleep(1)


def listener():
    Db.execute(query='LISTEN "{}";'.format(os.environ["CONSOLE_ID"]))
    logger.info(
        'Waiting for notifications on channel "{}";'.format(os.environ["CONSOLE_ID"])
    )

    while True:
        Db.conn.poll()
        while Db.conn.notifies:
            notify = Db.conn.notifies.pop(0)
            logger.info(
                "Got NOTIFY:{} {} {}".format(notify.pid, notify.channel, notify.payload)
            )

            payload = json.loads(notify.payload)
            operation = payload["operation"]
            message = payload["message"]

            if operation in ["INSERT", "UPDATE"]:
                msg = MsgAnalyzer(**message)
                msg.analyze_and_exec()


def main():
    # Set all device to last status
    get_last_completed_jobs = """
                    SELECT id, line_task_id, line_id, device_id, desired_state, exec_time, expire_time, status
                    FROM (
                    SELECT
                        ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY expire_time desc) AS r,
                        t.*
                    FROM
                        jobs_queue t) jobs
                    WHERE
                    jobs.r <= 1 and jobs.expire_time <= (now() at time zone 'utc') and status = 'completed';"""

    messages = Db.execute(query=get_last_completed_jobs, method="fetchall")
    for _message in messages:
        msg = MsgAnalyzer(**_message)
        msg.analyze_and_exec()

    # l = threading.Thread(target=listener, daemon=True)
    # l.start()

    s = threading.Thread(target=scheduler_super_task, daemon=True)
    s.start()

    s.join()
    # l.join()

    # read about multipoc

if __name__ == "__main__":
    main()
