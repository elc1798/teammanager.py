from flask import Flask, render_template, request, session, redirect, url_for
import userdb

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if 'logged_in' in session and session['logged_in']:
            return redirect(url_for("manager"))
        else:
            return render_template("login.html")
    else:
        assert(request.method == "POST")
        if userdb.verify(request.form['username_in'], request.form['password_in']) > 0:
            session['logged_in'] = True
            session['username_hash'] = userdb.username_hash(request.form['username_in']) # TODO FOR ETHAN
            session['password_hash'] = userdb.password_hash(request.form['password_in']) # TODO FOR ETHAN
            session["admin"] = userdb.verify(request.form['username_in'], request.form['password_in']) - 1:
            return redirect(url_for("manager"))
        else:
            session['logged_in'] = False
            return render_template("login.html", ERROR="User not recognized.")

@app.route("/manager/check/<student>")
@app.route("/manager/check/<student>/")
def manager(student="no_user"):
    if 'logged_in' not in session or not in session['logged_in']:
        return redirect(url_for("login"))
    if student == "no_user":
        return redirect(url_for("login"))
    if userdb.check_user() == 1 : # TODO FOR ETHAN
        return render_template("student_dashboard.html", STUDENT=student)
    elif userdb.check_user() == 2:
        return render_template("admin_dashboard.html")

@app.route("/manager/add_user")
@app.route("/manager/add_user/")
def add_user(): # TODO ETHAN
    if userdb.check_user() == 2:

@app.route("/logout")
@app.route("/logout/")
def logout():
    session['logged_in'] = False
    return redirect(url_for("login"))
