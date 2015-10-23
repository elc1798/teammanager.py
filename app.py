from flask import Flask, render_template, request, session, redirect, url_for
import userdb

app = Flask(__name__)

@app.route("/studentcheck")
@app.route("/studentcheck/")
def student_check():
    # Verify that session contains a student ID
    if 'sid' not in session:
        session.clear()     # Clear the session for a clean start
        return redirect(url_for("studentlogin"))
    else:
        info = userdb.get_user_data(session['sid'])
        return render_template("student_dashboard.html", INFO=info)

@app.route("/admincheck", methods=["GET", "POST"])
@app.route("/admincheck/", methods=["GET", "POST"])
@app.route("/admincheck/<sid>", methods=["GET", "POST"])
@app.route("/admincheck/<sid>/", methods=["GET", "POST"])
def admin_console(sid=-1):
    # Verify that session contains username, password, and admin field
    if "username" not in session or "password" not in session or "admin" not in session:
        session.clear()
        return redirect(url_for("studentlogin"))
    # Security checks...
    if not userdb.is_admin(session['username'], session['password']):
        session.clear()
        return redirect(url_for("studentlogin"))
    if not session['admin']:
        session.clear()
        return redirect(url_for("studentlogin"))
    if not userdb.id_exists(sid):
        if request.method == "GET":
            return render_template("admin_dashboard.html")
        else:
            # Sanity check
            assert(request.method == "POST")
            # The form on the admin console is the filter.
            # Check for each field from the form
            # TODO
            return render_template("admin_dashboard.html", FILTER=request.form)
    else:
        return render_template("admin_view_student.html",
                INFO=userdb.get_user_data(sid))

@app.route("/admin/adduser", methods=["GET", "POST"])
@app.route("/admin/adduser/", methods=["GET", "POST"])
def adduser():
    if request.method == "GET":
        if "username" not in session or "password" not in session or "admin" not in session:
            session.clear()
            return redirect(url_for("studentlogin"))
        # Security checks
        if not userdb.is_admin(session['username'], session['password']):
            session.clear()
            return redirect(url_for("studentlogin"))
        if not session['admin']:
            session.clear()
            return redirect(url_for("studentlogin"))

    elif request.method == "POST":
        form = request.form
        required_keys = ["sid", "last_name", "first_name", "email", "cell", "osis", "dob",
            "grad_year", "home_phone", "mother", "father", "mother_email", "father_email", "mother_cell", "father_cell", "pref_lang"]
        for key in required_keys:
            if key in form and form[key] != "":
                continue
            else:
                return render_template("add_user.html", ERROR="Some information is missing")

        sid = form["sid"]
        last_name = form["last_name"]
        first_name = form["first_name"]
        email = form["email"]
        cell = form["cell"]
        osis = form["osis"]
        dob = form["dob"]
        grad_year = form["grad_year"]
        home_phone = form["home_phone"]
        mother = form["mother"]
        mother_email = form["mother_email"]
        mother_cell = form["mother_cell"]
        father = form["father"]
        father_email = form["father_email"]
        father_cell = form["father_cell"]
        pref_lang = form["pref_lang"]

        data = []
        data.append(sid)
        data.append([last_name, first_name, email, cell])
        data.append([osis, dob, grad_year])
        data.append([mother, father, mother_email, father_email, home_phone, mother_cell, father_cell, pref_lang])
        userdb.add_user(data)

    return render_template("add_user.html")

# Methods for Login System

@app.route("/adminlogin", methods=["GET", "POST"])
@app.route("/adminlogin/", methods=["GET", "POST"])
def adminlogin():
    # If the request method is GET, then it's not the form
    if request.method == "GET":
        # If user is already logged in, bring them to manager based on access
        # level.
        if 'logged_in' in session and session['logged_in']:
            # If the admin field is true, return admin console
            if 'admin' in session and session['admin']:
                return redirect(url_for("admin_console"))
            # Otherwise,return the student console for the student ID
            else:
                return redirect(url_for("student_check"))
        # If the user isn't logged in, render the student login page by default
        else:
            return render_template("admin_login.html")
    # The request method should be POST
    else:
        # Sanity Check
        assert(request.method == "POST")

        last_name = str(request.form['last_name'])
        sid = request.form['sid']
        try:
            sid = int(sid)
        except:
            return render_template("admin_login.html", ERROR="Invalid 4-digit ID")

        # Check if valid user
        if userdb.is_admin(last_name, sid):
            session['logged_in'] = True         # Set logged in to True
            session['admin'] = True             # Set admin to True
            session['username'] = last_name     # Set last_name variable
            session['password'] = sid           # Set sid variable
            return redirect(url_for("admin_console"))
        else:
            return render_template("admin_login.html", ERROR="Unknown User")


# Student login
@app.route("/", methods=["GET", "POST"])
@app.route("/studentlogin", methods=["GET", "POST"])
@app.route("/studentlogin/", methods=["GET", "POST"])
def studentlogin():
    # If the request method is GET, then it's not the form
    if request.method == "GET":
        # If user is already logged in, bring them to manager based on access
        # level.
        if 'logged_in' in session and session['logged_in']:
            # If the admin field is true, return admin console
            if 'admin' in session and session['admin']:
                return redirect(url_for("admin_console"))
            # Otherwise,return the student console for the student ID
            else:
                return redirect(url_for("student_check"))
        # If the user isn't logged in, render the student login page by default
        else:
            return render_template("student_login.html")
    # The request method should be POST
    else:
        # Sanity Check
        assert(request.method == "POST")
        last_name = str(request.form['last_name'])
        sid = request.form['sid']
        # If sid is NaN, then immediately kill. Kill it with fire.
        try:
            sid = int(sid)
        except:
            return render_template("student_login.html", ERROR="Invalid 4-digit ID")
        # Check if valid user
        if userdb.user_exists(last_name, sid):
            session['logged_in'] = True         # Set logged in to True
            session['last_name'] = last_name    # Set last_name variable
            session['sid'] = sid                # Set sid variable
            return redirect(url_for("student_check"))
        else:
            return render_template("student_login.html", ERROR="Unknown User")

@app.route("/logout")
@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("studentlogin"))

if __name__ == "__main__":
    try:
        f = open("app_secret_key")
        app.secret_key = str(f.readline())
    except:
        exit()
    app.debug = True
    app.run(host='0.0.0.0', port=4567)
