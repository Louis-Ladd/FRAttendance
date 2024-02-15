from flask import Flask 

from .events import socketio
from .routes import main
from .updater import updateThread

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "secret!"

    app.register_blueprint(main)

    thread = updateThread()
    thread.start()

    socketio.init_app(app)

    return app
