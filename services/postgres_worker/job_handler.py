import threading, time, signal
from resources.db import Db

from datetime import timedelta
import logging
from models.device import Device

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message(message):
    device = Device.get_by_id(message["device_id"])
    device.state = dict(desired_state=message["desired_device_state"])


WAIT_TIME_SECONDS = 60

class ProgramKilled(Exception):
    pass

def check_and_run():
    get_last_completed_jobs = """ SELECT line_task_id,
                     line_id,
                     device_id,
                     desired_device_state,
                     exec_time
                     FROM jobs_queue
                     WHERE state = 'completed'
                     AND exec_time <= now()
                     ORDER BY exec_time DESC"""

    queue = Db.execute(query=get_last_completed_jobs, method="fetchall")
    for message in queue:
        send_message(message)
    
def signal_handler(signum, frame):
    raise ProgramKilled
    
class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        
    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(*self.args, **self.kwargs)
            
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=check_and_run)
    job.start()
    
    while True:
          try:
              time.sleep(1)
          except ProgramKilled:
              print("Program killed: running cleanup code")
              job.stop()
              break