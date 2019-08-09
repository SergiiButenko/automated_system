from web.helpers.create_app import create_jwt_app, create_flask_app
from web.views import auth, devices, groups, tasks
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app, socketio = create_flask_app(__name__)
jwt = create_jwt_app(app=app)

app.register_blueprint(devices, url_prefix="/v1/devices")
app.register_blueprint(auth, url_prefix="/v1/auth")
app.register_blueprint(groups, url_prefix="/v1/groups")
app.register_blueprint(tasks, url_prefix="/v1/tasks")


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
