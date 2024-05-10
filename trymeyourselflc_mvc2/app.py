import os
from flask import Flask, session,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from controllers import index, dashboard_trainer, dashboard_trainee, dashboard_admin, register, login, logout
from models import db

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://test01:test@01@localhost/tmys"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
@app.route("/index")
@app.route("/login/index")
def index_route():
    return index()

@app.route("/Trainer/Dashboard")
def dashboard_trainer_route():
    return dashboard_trainer()

@app.route("/Trainee/Dashboard")
def dashboard_trainee_route():
    return dashboard_trainee()

@app.route("/Admin/Dashboard")
def dashboard_admin_route():
    return dashboard_admin()

@app.route("/register")
def register_route():
    return register()

@app.route("/login", methods=["GET", "POST"], endpoint="login_route")
def login_route():
    # return login()
    return login()

@app.route("/logout")
def logout_route():
    return logout()

if __name__ == "__main__":
    app.run(debug=True)
