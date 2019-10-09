import paho.mqtt.client as mqtt
import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _Mosquitto:
    @staticmethod
    def _on_disconnect(client, userdata, rc):
        logging.debug("DisConnected result code "+str(rc))
        client.loop_stop()

    def _on_connect(self, userdata, flags, rc):
        logger.debug("Connected With Result Code {}".format(rc))

    @staticmethod
    def _on_message(userdata, message):
        logger.info(message.payload.decode())
        logger.info(message.topic)

    def __init__(self):
        broker_address = str(os.environ["MOSQUITTO_HOST"])
        broker_portno = int(os.environ["MOSQUITTO_PORT"])
        self.client = mqtt.Client()

        logger.info("Connecting to mqtt broker")
        self.client.on_connect = _Mosquitto._on_connect
        self.client.on_disconnect = _Mosquitto._on_disconnect
        self.client.on_message = _Mosquitto._on_message

        self.client.connect(broker_address, broker_portno)

    def send_message(self, topic, payload):
        return self.client.publish(topic=topic, payload=payload)

    def subscribe(self, topic):
        logger.info("Subscribing to {} topic".format(topic))
        self.client.subscribe(topic)
        self.client.loop_start()


Mosquitto = _Mosquitto()
