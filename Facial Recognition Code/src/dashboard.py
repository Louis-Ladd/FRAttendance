from flask import Flask
from flask import request
from flask import render_template

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
    return render_template("server.html")


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