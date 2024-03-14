'''
File: routes.py
Purpose: Handle main routes
Note: All of these routes require login for access
Project: FRAttendance
File Created: Thursday, 14th March 2024 12:25:28 pm
Author: Louis Harshman (lewisharshman1@gmail.com)
-----
Last Modified: Thursday, 14th March 2024 3:47:31 pm
Modified By: Louis Harshman (lewisharshman1@gmail.com)
-----
Copyright 2019 - 2024
'''

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from flask import request, jsonify

from .updater import server_info
from . import school_db
from .models import User

main = Blueprint("main", __name__)

MESSAGE_404= "HTTP 404 Error: The page you are looking for does not exist"
MESSAGE_401= "HTTP 401 Error: You are not authorized to make that request"


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
    if not current_user.isAdmin:
        return MESSAGE_401, 401
    return render_template("server.html", server_info=server_info)


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

@main.route("/accounts")
@login_required
def accounts():
    if not current_user.isAdmin:
        return MESSAGE_401, 401
    return render_template("accounts.html")

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
        return MESSAGE_401, 401
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

# USERS ROUTES: For accessing or mutating the data of OTHER users
# Only administrators should be able to do this.

@main.route ("/users/addClass", methods=["POST"])
@login_required
def user_add_class():
    if not current_user.isAdmin:
        return MESSAGE_401, 401
    username = request.form.get("username")
    class_name = request.form.get("class_name")
    result = current_user.add_class_to_user(class_name, username)
    return result

@main.route ("/users/removeClass", methods=["POST"])
@login_required
def user_remove_class():
    if not current_user.isAdmin:
        return MESSAGE_401, 401
    username = request.form.get("username")
    class_name = request.form.get("class_name")
    result = current_user.remove_class_from_user(class_name, username)
    return result 

@main.route ("/users/deleteUser", methods=["POST"])
@login_required
def user_delete():
    if not current_user.isAdmin:
        return MESSAGE_401, 401
    return "NO", 200
    username = request.get_json()["username"] 
    result = current_user.delete_user(username)
    return result

@main.route ("/users/getUsers", methods=["GET"])
@login_required
def user_get_classes():
    # TODO: DO NOT SEND PASSWORDS HASHED, EVEN FOR ADMINISTRATORS, THEY SHOULD NOT BE ABLE TO ACCESS PASSWORDS. - Louis
    if not current_user.isAdmin:
        return MESSAGE_401, 401
    users = User.query.all()
    users_dict = {"username": [], "name": [], "classes": [], "isAdmin": []}
    for user in users:
        users_dict["username"].append(user.username)
        users_dict["name"].append(user.name)
        users_dict["classes"].append(user.get_classes())
        users_dict["isAdmin"].append(user.isAdmin)
    return users_dict

# USER ROUTE: For accessing or mutating the data of the current user
# All users should be able to do this BUT strict checks should ensure that data ownership is respected.

@main.route("/user/getClasses", methods=["GET"])
@login_required
def current_user_get_classes():
    return current_user.get_classes()

@main.route("/user/getUsername", methods=["GET"])
@login_required
def current_user_get_user():
    return jsonify({"username" : current_user.username, "name" : current_user.name}) 