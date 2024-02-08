from flask import Flask
from flask import request
from flask import render_template
from flask_socketio import SocketIO, emit
import socket
import psutil
import threading
from threading import Thread

VERBOSE = False

hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)
server_info = {"ip" : socket.gethostbyname(hostname), "hostname" : hostname, "cpu_usage" : [], "ram_usage" : []}
server_info["cpu_usage"].append(psutil.cpu_percent(4))
server_info["ram_usage"].append(psutil.virtual_memory().percent)

app = Flask(__name__)   
app.config["SECRET_KEY"] = "secret!"  
socketio = SocketIO(app)

def debug_log(x):
    if VERBOSE:
        print(x)

class updateThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stopped = threading.Event()
        self.daemon = True

    def run(self):
        while not self.stopped.wait(0.25):
            debug_log(f"Fetching CPU Usage...")
            server_info["cpu_usage"].append(psutil.cpu_percent(0))
            server_info["ram_usage"].append(psutil.virtual_memory().percent)
            debug_log(f"CPU Usage updated: {server_info['cpu_usage'][-1]}")

thread = updateThread()
thread.start()


@socketio.on("connect")
def handle_connect():
    print("SocketIO Connection: client connected")
    emit("info_update", server_info)

@socketio.on("refresh")
def refresh_server_info():
    emit("info_update", server_info)

@app.route("/")
def home():
    return render_template("index.html", username=request.remote_addr)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/server")
def server():
    return render_template("server.html", server_info=server_info)


@app.route("/cameras")
def camears():
    return render_template("cameras.html")


@app.route("/classes")
def classes():
    return render_template("classes.html")


@app.route("/notifications")
def notifications():
    return render_template("notifications.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
