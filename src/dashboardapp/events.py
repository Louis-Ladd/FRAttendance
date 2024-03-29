from flask_socketio import emit

from .extensions import socketio
from .updater import server_info

@socketio.on("connect")
def handle_connect():
    print("SocketIO Connection: client connected")
    emit("info_update", server_info)

#This event is ment to be looped from the client side
@socketio.on("refresh")
def refresh_server_info():
    emit("info_update", server_info)