from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from .updater import server_info

main = Blueprint("main", __name__)

@main.route("/")
@login_required
def root():
    return redirect(url_for("main.home"))

@main.route("/home")
@login_required
def home():
    return render_template("index.html", username=current_user.name)

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@main.route("/server")
@login_required
def server():
    if current_user.isAdmin:
        return render_template("server.html", server_info=server_info)
    return "You do not have permission to view this page"

@main.route("/cameras")
@login_required
def camears():
    #TODO: be prepared to pipe a lot of information from backend to frontend
    return render_template("cameras.html")

@main.route("/classes")
@login_required
def classes():
    return render_template("classes.html")

@main.route("/notifications")
@login_required
def notifications():
    return render_template("notifications.html")
