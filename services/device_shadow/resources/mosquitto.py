import paho.mqtt.client as mqtt
import os, time, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _Mosquitto:
    @staticmethod
    def _on_disconnect(client, userdata, rc):
        logging.debug("DisConnected result code "+str(rc))
        client.loop_stop()

    @staticmethod
    def _on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True
            logger.info("connected OK Returned code=" + str(rc))
        else:
            logger.info("Bad connection Returned code=" + str(rc))

    @staticmethod
    def _on_message(client, userdata, message):
        logger.info("message received "+str(message.payload.decode("utf-8")))
        logger.info("message topic="+str(message.topic))
        logger.info("message qos="+str(message.qos))
        logger.info("message retain flag="+str(message.retain))

    def __init__(self):
        broker_address = str(os.environ["MOSQUITTO_HOST"])
        broker_portno = int(os.environ["MOSQUITTO_PORT"])
        self.client = mqtt.Client()
        self.client.connected_flag = False

        logger.info("Connecting to mqtt broker")
        self.client.on_connect = _Mosquitto._on_connect
        self.client.on_disconnect = _Mosquitto._on_disconnect
        self.client.on_message = _Mosquitto._on_message

        self.client.connect(broker_address, broker_portno)
        # while not self.client.connected_flag:
        #     time.sleep(1)
        self.client.loop_start()
    
    def __del__(self):
        logger.info("del")
        if self.client is not None:
            logger.info("colsing connection")
            self.client.loop_stop()
            self.client.disconnect()

    def send_message(self, topic, payload):
        return self.client.publish(topic=topic, payload=payload)

    def subscribe(self, topic):
        logger.info("Subscribing to {} topic".format(topic))
        self.client.subscribe(topic)


Mosquitto = _Mosquitto()
