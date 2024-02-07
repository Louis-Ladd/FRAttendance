from flask import Flask
from flask import request
from flask import render_template
import socket
import psutil
import threading
from threading import Thread

VERBOSE = False

hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)
server_info = {"IP" : socket.gethostbyname, "hostname" : hostname, "CPU_USAGE" : []}
server_info["CPU_USAGE"].append(psutil.cpu_percent(4))

def debug_log(x):
    if VERBOSE:
        print(x)

class updateThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stopped = threading.Event()
        self.daemon = True

    def run(self):
        while not self.stopped.wait(1):
            debug_log(f"Fetching CPU Usage...")
            server_info["CPU_USAGE"].append(psutil.cpu_percent(4))
            debug_log(f"CPU Usage updated: {server_info['CPU_USAGE'][-1]}")

thread = updateThread()
thread.start()

app = Flask(__name__)     

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
    app.run(debug=True)
