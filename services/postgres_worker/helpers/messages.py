from models.device import Device


def send_message(message):
    device = Device.get_by_id(message['device_id'])
    device.state = dict(desired_state=message['desired_device_state'])

