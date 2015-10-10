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
        if userdb.verify(request.form['username_in'], request.form['password_in']):
            session['logged_in'] = True
            session['username_hash'] = userdb.username_hash(request.form['username_in'])
            session['password_hash'] = userdb.password_hash(request.form['password_in'])
            return redirect(url_for("

