from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from flask import request, jsonify

from .updater import server_info
from . import school_db

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
    return render_template("dashboard.html", user_classes=current_user.get_classes())

@main.route("/server")
@login_required
def server():
    if current_user.isAdmin:
        return render_template("server.html", server_info=server_info)
    return "HTTP 401 Erorr: You are unauthorized to view this page", 401


@main.route("/cameras")
@login_required
def camears():
    # TODO: be prepared to pipe a lot of information from backend to frontend
    return render_template("cameras.html")


@main.route("/classes")
@login_required
def classes():
    return render_template("classes.html")

@main.route("/notifications")
@login_required
def notifications():
    return render_template("notifications.html")

### Get/Post routes for various database and backend functionality ###

@main.route("/database/getClasses")
@login_required
def get_classes():
    return school_db.get_classes()

@main.route("/database/getClass/<jsdata>")
@login_required
def get_javascript_data(jsdata=None):
    return school_db.get_class(jsdata)

@main.route("/database/getClass/<jsdata>/<top>")
@login_required
def get_javascript_data_top(jsdata=None, top=None):
    return school_db.get_class(jsdata, top=int(top))

@main.route("/database/createStudent", methods=["POST"])
@login_required
def create_student():
    # Learn how post forms work and that'll make this easier to implement.
    # You can copy how it was implemented in ./templates/login.html ln 23-37 and ./auth.py ln 17-30
    # rewrite and implement it into classes after learning how it works. - Louis
    if not current_user.isAdmin:
        return "HTTP 401 Error: You are unauthorized to do that", 401
    first_name = request.form.get("first_name")  # Changed from "first_name" to "name"
    last_name = request.form.get("last_name")
    print(f"'Made' the student {first_name} {last_name}")
    return redirect(url_for("main.classes"))
    if not first_name or not last_name:
        return "Missing student name", 400
    student_id = school_db.create_student(first_name, last_name)
    if student_id is not None:
        return redirect(url_for("main.classes"))
    else:
        return "Failed to create student", 500
    
@main.route ("/users/addClass", methods=["POST"])
@login_required
def user_add_class():
    if not current_user.isAdmin:
        return "HTTP 401 Error: You are unauthorized to do that", 401
    username = request.form.get("username")
    class_name = request.form.get("class_name")
    result = current_user.add_class_to_user(class_name, username)
    return result

@main.route ("/users/removeClass", methods=["POST"])
@login_required
def user_remove_class():
    if not current_user.isAdmin:
        return "HTTP 401 Error: You are unauthorized to do that", 401
    username = request.form.get("username")
    class_name = request.form.get("class_name")
    result = current_user.remove_class_from_user(class_name, username)
    return result 

@main.route("/users/getClasses", methods=["GET"])
@login_required
def current_user_get_classes():
    return jsonify(current_user.get_classes())