from flask import Blueprint, render_template, request

from .updater import server_info

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html", username=request.remote_addr)

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@main.route("/server")
def server():
    return render_template("server.html", server_info=server_info)

@main.route("/cameras")
def camears():
    return render_template("cameras.html")

@main.route("/classes")
def classes():
    return render_template("classes.html")

@main.route("/notifications")
def notifications():
    return render_template("notifications.html")
