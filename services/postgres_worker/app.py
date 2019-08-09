import json
import logging
import os
from datetime import datetime

from resources.db import Db
from helpers.messages import send_message


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def loop():
    # Initial job execution

    get_jobs = """ SELECT line_task_id,
                     line_id,
                     device_id,
                     desired_device_state,
                     exec_time
                     FROM jobs_queue
                     WHERE state = 'pending'
                     AND exec_time >= now() - INTERVAL '1 HOUR'
                     AND exec_time <= now()
                     ORDER BY exec_time DESC"""

    queue = Db.execute(query=get_jobs, method='fetchall')
    for message in queue:
        send_message(message)

    # start listening
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
            operation = payload['operation']
            message = payload['record']
            # parse time
            message['exec_time'] = message['exec_time']

            logger.info("message {}".format(message))

            if operation in ['INSERT', 'UPDATE']: #and message['exec_time'] <= datetime.now(timezone.utc):
                send_message(message)


if __name__ == "__main__":
    loop()
