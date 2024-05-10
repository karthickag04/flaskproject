from flask import render_template, request, redirect, url_for, session
from models import User

def index():
    return render_template("Login/Index.html", title="Index")

def dashboard_trainer():
    return render_template("Trainer/Dashboard.html", title="Trainer Dashboard")

def dashboard_trainee():
    return render_template("Trainee/Dashboard.html", title="Trainee Dashboard")

def dashboard_admin():
    return render_template("Admin/Dashboard.html", title="Admin Dashboard")

def register():
    return render_template("Login/Register.html", title="Register")

def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check tbl_login table for user
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = user.username
            session['jobrole'] = user.jobrole

            if user.jobrole == "Trainer":
                return redirect(url_for('dashboard_trainer'))
            elif user.jobrole == "Admin":
                print("Login success with " + user.jobrole)
                return redirect(url_for('dashboard_admin'))

        # Check tbl_reg_users table if user is not found in tbl_login
        user1 = User.query.filter_by(username=username, password=password).first()

        if user1:
            session['username'] = user1.username
            session['jobrole'] = user1.jobrole
            return redirect(url_for('dashboard_trainee'))

        # If neither user nor user1 exists, render login page again
        return render_template("Login/Login.html", title="Login")

    # Render the login form for GET requests
    return render_template("Login/Login.html", title="Login")

def logout():
    # Clear session data
    session.clear()
    # Redirect to the login page
    return redirect(url_for('index'))
