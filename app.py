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

@app.route("/admincheck")
@app.route("/admincheck/<sid>")
def admin_console(sid=-1):
    # Verify that session contains username, password, and admin field
    if "username" not in session or "password" not in session or "admin" not in session:
        session.clear()
        return redirect(url_for("studentlogin"))
    # Security checks...
    if not userdb.is_admin(session['username'], session['password']):
        session.clear()
        return redirect(url_for("studentlogin"))
    if not sesson['admin']:
        session.clear()
        return redirect(url_for("studentlogin"))
    if not userdb.id_exists(sid):
        return render_template("admin_dashboard.html")
    else:
        return render_template("admin_dashboard.html",
                INFO=userdb.get_user_data(sid))

# Methods for Login System

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
            # Assert that "admin" key is in the session. It SHOULD be, but you
            # never know
            if 'admin' not in session:
                return render_template("student_login.html")
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

