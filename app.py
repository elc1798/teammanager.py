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
        if userdb.check_user(request.form['username_in'], request.form['password_in']) > 0:
            session['logged_in'] = True
            session['username'] = request.form['username_in']
            session['password'] = request.form['password_in']
            session['admin'] = userdb.check_user(request.form['username_in'], request.form['password_in']) - 1
            return redirect(url_for("manager"))
        else:
            session['logged_in'] = False
            return render_template("login.html", ERROR="User not recognized.")

@app.route("/manager")
@app.route("/manager/")
@app.route("/manager/check/<student>")
@app.route("/manager/check/<student>/")
def manager(student="no_user"):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for("login"))
    if student == "no_user":
        return redirect(url_for("login"))
    if session['admin'] == 0:
        return render_template("student_dashboard.html", STUDENT=student)
    elif session['admin'] == 1:
        return render_template("admin_dashboard.html")

@app.route("/manager/add_user")
@app.route("/manager/add_user/")
def add_user():
    if 'logged_in' not in session or not session['logged_in'] or session['admin'] == 0:
        return redirect(url_for("manager"));
    if request.method == "GET":
        return render_template("add_user.html")
    else:
        data = []
        data.append(request.form['new_name'])
        data.append(request.form['new_sid'])
        data.append(request.form['new_email'])
        data.append(request.form['new_cell'])
        try:
            data.append(int(request.form['new_grad_year']))
        except:
            return render_template("add_user.html", ERROR="Invalid Graduation Year")
        data.append(0)
        data.append(0)
        data.append(request.form['mother_name'])
        data.append(request.form['father_name'])
        data.append(request.form['parent_email'])
        data.append(request.form['home_phone'])
        data.append(request.form['cell_phone'])
        data.append(request.form['pref_lang'])
        userdb.add_user(data)
        return redirect(url_for("manager"));

@app.route("/logout")
@app.route("/logout/")
def logout():
    session['logged_in'] = False
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.secret_key = 'dcb61f28eafb8771213f3e0612422b8d'
    app.debug = True
    app.run(host='0.0.0.0', port=4567)

