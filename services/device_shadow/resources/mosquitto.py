import paho.mqtt.client as mqtt
import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Mosquitto:
    def __init__(self, on_message, on_connect, on_disconnect, topic):
        broker_address = os.environ["MOSQUITTO_HOST"]
        broker_portno = os.environ["MOSQUITTO_PORT"]
        self.topic=topic
        self.client = mqtt.Client(topic)

        logger.info("Connecting to mqtt broker")
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message

        self.client.connect(broker_address, broker_portno)

    def send_message(self, payload):
        return self.client.publish(topic=self.topic, payload=payload)

    def listen(self):
        self.client.subscribe(self.topic)
        self.client.loop_forever()
