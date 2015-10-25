from flask import Flask, render_template, request, session, redirect, url_for, flash
from functools import wraps
import userdb

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session or not session['logged_in'] \
                or "last_name" not in session \
                or "sid" not in session:
            session.clear()
            return redirect(url_for("studentlogin"))
	return f(*args, **kwargs)
    return decorated_function

def admins_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session or not session['admin']:
            session.clear()
            return redirect(url_for("studentlogin"))
	return f(*args, **kwargs)
    return decorated_function

def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            # If the admin field is true, return admin console
            if 'admin' in session and session['admin']:
                return redirect(url_for("admin_console"))
            # Otherwise,return the student console for the student ID
            else:
                return redirect(url_for("student_check"))
	return f(*args, **kwargs)
    return decorated_function

@app.route("/studentcheck")
@app.route("/studentcheck/")
@login_required
def student_check():
    info = userdb.get_user_data(session['sid'])
    return render_template("student_dashboard.html", INFO=info)

@app.route("/admincheck", methods=["GET", "POST"])
@app.route("/admincheck/", methods=["GET", "POST"])
@app.route("/admincheck/<sid>", methods=["GET", "POST"])
@app.route("/admincheck/<sid>/", methods=["GET", "POST"])
@login_required
@admins_only
def admin_console(sid=-1):
    if not userdb.id_exists(sid):
        if request.method == "GET":
            return render_template("admin_dashboard.html")
        else:
            # Sanity check
            assert(request.method == "POST")
            # The form on the admin console is the filter.
            filtered = userdb.get_data_with_filter(request.form)
            # If get_data_with_filter returns an empty dictionary
            if not filtered:
                flash("No users meet the criteria", "danger")
                return render_template("admin_dashboard.html")
            else:
                flash("Here are the results:", "success")
                return render_template("admin_dashboard.html", users=filtered)
    else:
        return render_template("admin_view_student.html",
                INFO=userdb.get_user_data(sid))

@app.route("/admin/adduser", methods=["GET", "POST"])
@app.route("/admin/adduser/", methods=["GET", "POST"])
@login_required
@admins_only
def adduser():
    if request.method == "POST":
        form = request.form
        required_keys = ["sid", "last_name", "first_name", "email", "cell", "osis", "dob",
            "grad_year", "home_phone", "mother", "father", "mother_email", "father_email", "mother_cell", "father_cell", "pref_lang"]
        for key in required_keys:
            if key in form and form[key] != "":
                continue
            else:
                flash("Some information is missing", "danger")
                break

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
@redirect_if_logged_in
def adminlogin():
    if request.method == "POST":
        last_name = str(request.form['last_name'])
        sid = request.form['sid']
        try:
            sid = int(sid)
        except:
            flash("Invalid 4-digit ID", "danger")

        # Check if valid user
        if userdb.is_admin(last_name, sid):
            session['logged_in'] = True         # Set logged in to True
            session['admin'] = True             # Set admin to True
            session['last_name'] = last_name    # Set last_name variable
            session['sid'] = sid                # Set sid variable
            return redirect(url_for("admin_console"))
        else:
            flash("Unknown User", "danger")

    return render_template("admin_login.html")


# Student login
@app.route("/", methods=["GET", "POST"])
@app.route("/studentlogin", methods=["GET", "POST"])
@app.route("/studentlogin/", methods=["GET", "POST"])
def studentlogin():
    if request.method == "POST":
        last_name = str(request.form['last_name'])
        sid = request.form['sid']
        # If sid is NaN, then immediately kill. Kill it with fire.
        try:
            sid = int(sid)
        except:
            flash("Invalid 4-digit ID", "danger")
        # Check if valid user
        if userdb.user_exists(last_name, sid):
            session['logged_in'] = True         # Set logged in to True
            session['last_name'] = last_name    # Set last_name variable
            session['sid'] = sid                # Set sid variable
            return redirect(url_for("student_check"))
        else:
            flash("Unknown User", "danger")
    return render_template("student_login.html")

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
