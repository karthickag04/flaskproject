import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app=Flask(__name__)

app.secret_key = os.urandom(24)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="test01"
app.config["MYSQL_PASSWORD"]="test@01"
app.config["MYSQL_DB"]="tmys"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


@app.route("/")
@app.route("/index")
@app.route("/login/index")
def index():
    return render_template("Login/Index.html")



@app.route("/Trainer/Dashboard")
def DashboardTrainer():
    return render_template("Trainer/Dashboard.html")

@app.route("/Trainee/Dashboard")
def DashboardTrainee():
    return render_template("Trainee/Dashboard.html")

@app.route("/Admin/Dashboard")
def DashboardAdmin():
    return render_template("Admin/Dashboard.html")


@app.route("/register")
def register():
    return render_template("Login/Register.html")

# @app.route("/login")
# def login():
#     return render_template("Login/Login.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Check tbl_login table for user
        conn = mysql.connection.cursor()
        conn.execute("SELECT * FROM tbl_login WHERE username=%s AND password=%s", (username, password))
        user = conn.fetchone()
        conn.close()
        
        if user:
            # Store user's username and jobrole in session
            session['username'] = user['username']  # Assuming username is the second item in the user tuple
            session['jobrole'] = user['jobrole']  # Assuming jobrole is the third item in the user tuple

            # Check user jobrole and redirect accordingly
            if user['jobrole'] == "Trainer":
                return redirect(url_for('DashboardTrainer'))
            elif user['jobrole'] == "Admin":
                print("login success with "+"  "+user['jobrole'])
                return redirect(url_for('DashboardAdmin'))
        
        # Check tbl_reg_users table if user is not found in tbl_login
        conn = mysql.connection.cursor()
        conn.execute("SELECT * FROM tbl_reg_users WHERE username=%s AND password=%s", (username, password))
        user1 = conn.fetchone()
        conn.close()
        
        if user1:
            # Store user's username and jobrole in session
            session['username'] = user1['username']  # Assuming username is the second item in the user1 tuple
            session['jobrole'] = user['jobrole']  # Assuming UserType is the fourth item in the user1 tuple

            # Redirect to Trainee dashboard
            return redirect(url_for('DashboardTrainee'))

        # If neither user nor user1 exists, render login page again
        return render_template("Login/Login.html")
    
    # Render the login form for GET requests
    return render_template("Login/Login.html")

@app.route("/logout")
def logout():
    # Clear session data
    session.clear()
    # Redirect to the login page
    return redirect(url_for('index'))

    

if __name__ == "__main__":
    app.run(debug=True)