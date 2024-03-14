'''
File: events.py
Purpose: Handle socket.io events
Project: FRAttendance
File Created: Thursday, 14th March 2024 12:25:28 pm
Author: Louis Harshman (lewisharshman1@gmail.com)
-----
Last Modified: Thursday, 14th March 2024 3:46:35 pm
Modified By: Louis Harshman (lewisharshman1@gmail.com)
-----
Copyright 2019 - 2024
'''

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