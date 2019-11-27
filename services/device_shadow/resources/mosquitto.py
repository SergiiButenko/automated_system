import paho.mqtt.client as mqtt
import os, time, logging, json
from .devices import Devices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _Mosquitto:
    @staticmethod
    def _on_disconnect(client, userdata, rc):
        logging.debug("DisConnected result code " + str(rc))
        client.loop_stop()

    @staticmethod
    def _on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("connected OK Returned code=" + str(rc))
        else:
            logger.info("Bad connection Returned code=" + str(rc))

    @staticmethod
    def _on_message(client, userdata, message):
        msg = message.payload.decode("utf-8")
        logger.info("message received " + str(msg))
        logger.info("message topic=" + str(message.topic))
        try:
            msg = json.loads(msg)
        except Exception:
            logger.error("Reseived message is not a JSON")
            return

        device = Devices.get_by_id(msg['device_id'])

        for _line in msg['lines'].items():
            device.set_line_state_by_relay_num(_line['actual_state'])

        
    def __init__(self):
        broker_address = str(os.environ["MOSQUITTO_HOST"])
        broker_portno = int(os.environ["MOSQUITTO_PORT"])
        self.client = mqtt.Client()

        logger.info("Connecting to mqtt broker")
        self.client.on_connect = _Mosquitto._on_connect
        self.client.on_disconnect = _Mosquitto._on_disconnect
        self.client.on_message = _Mosquitto._on_message

        self.client.connect(broker_address, broker_portno)
        self.client.loop_start()

    def __del__(self):
        logger.info("del")
        if self.client is not None:
            logger.info("closing connection")
            self.client.loop_stop()
            self.client.disconnect()

    def send_message(self, topic, payload):
        return self.client.publish(topic=topic, payload=json.dumps(payload))

    def subscribe(self, topic):
        general_topic = str(topic) + '/+'
        logger.info("Subscribing to {} topic".format(general_topic))
        self.client.subscribe(general_topic)

Mosquitto = _Mosquitto()
