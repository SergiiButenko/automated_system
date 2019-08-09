from flask_socketio import emit
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message(channel, data):
    """Enclose emit method into try except block."""
    try:
        emit(channel, data)
        logger.info("Message was sent.")
        logger.info(data)
    except Exception as e:
        logger.error(e)
        logger.error("Can't send message. Exeption occured")
