import sqlite3

db_name = "users.db"

# Returns True if user exists in database given last name and student id
def user_exists(last_name, sid):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    PARAMS = (last_name , sid)
    QUERY = "SELECT * FROM students WHERE last_name = ? AND sid = ?;"
    result = list(c.execute(QUERY, PARAMS))
    conn.close()
    return len(result) == 1 # If > 1, then duplicate users

# Returns True if ID exists
def id_exists(sid):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    QUERY = "SELECT * FROM students WHERE sid = ?;"
    result = list(c.execute(QUERY, (sid,)))
    conn.close()
    return len(result) == 1

# Returns a dictionary containing the following keys, given a student id
#   "first_name"        string
#   "last_name"         string
#   "osis"              integer
#   "student_id"        integer
#   "student_email"     string
#   "student_cell"      long
#   "birthday"          string
#   "grad_year"         integer
#   "medicals"          boolean
#   "safety_test"       boolean
#   "team_dues"         boolean
#   "service_hours"     integer
#   "mother"            string
#   "father"            string
#   "mother_email"      string
#   "father_email"      string
#   "home_phone"        integer
#   "mother_cell"       integer
#   "father_cell"       integer
#   "pref_lang"         string
def get_user_data(sid):
    if not id_exists(sid):
        return {}
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    QUERY = "SELECT %s FROM %s WHERE sid = ?;"
    data = {}
    data["first_name"] = str(list(c.execute(QUERY % ("first_name",
        "students"),(sid,)))[0][0])
    data["last_name"] = str(list(c.execute(QUERY % ("last_name",
        "students"),(sid,)))[0][0])
    data["osis"] = int(list(c.execute(QUERY % ("osis",
        "student_data"),(sid,)))[0][0])
    data["student_id"] = sid
    data["student_email"] = str(list(c.execute(QUERY % ("email",
        "students"),(sid,)))[0][0])
    data["student_cell"] = int(list(c.execute(QUERY % ("cell",
        "students"),(sid,)))[0][0])
    data["birthday"] = str(list(c.execute(QUERY % ("DOB",
        "student_data"),(sid,)))[0][0])
    data["grad_year"] = int(list(c.execute(QUERY % ("grad_year",
        "student_data"),(sid,)))[0][0])
    data["medicals"] = str(list(c.execute(QUERY % ("medicals",
        "student_data"),(sid,)))[0][0])
    data["safety_test"] = int(list(c.execute(QUERY % ("safety_test",
        "student_data"),(sid,)))[0][0]) == 1
    data["team_dues"] = int(list(c.execute(QUERY % ("team_dues",
        "student_data"),(sid,)))[0][0]) == 1
    data["service_hours"] = int(list(c.execute(QUERY % ("service_hours",
        "student_data"),(sid,)))[0][0])
    data["mother"] = str(list(c.execute(QUERY % ("mother",
        "parent_data"),(sid,)))[0][0])
    data["father"] = str(list(c.execute(QUERY % ("father",
        "parent_data"),(sid,)))[0][0])
    data["mother_email"] = str(list(c.execute(QUERY % ("mother_email",
        "parent_data"),(sid,)))[0][0])
    data["home_phone"] = int(list(c.execute(QUERY % ("home_phone",
        "parent_data"),(sid,)))[0][0])
    data["mother_cell"] = int(list(c.execute(QUERY % ("mother_cell",
        "parent_data"),(sid,)))[0][0])
    data["father_cell"] = int(list(c.execute(QUERY % ("father_cell",
        "parent_data"),(sid,)))[0][0])
    data["pref_lang"] = str(list(c.execute(QUERY % ("pref_lang",
        "parent_data"),(sid,)))[0][0])
    conn.close()
    return data

# Adds a user into the database given a list
# data[0] should contain student_id
# data[1] should contain [last_name, first_name, email, cell]
# data[2] should contain [OSIS, DOB, grad_year]
# data[3] should contain [mother, father, mother_email, father_email,
# home_phone, mother_cell, father_cell, pref_lang]
def add_user(data):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    QUERY1 = "INSERT INTO students VALUES (?,?,?,?,?);"
    QUERY2 = "INSERT INTO student_data VALUES (?,?,?,?,?,?,?,?);"
    QUERY3 = "INSERT INTO parent_data VALUES (?,?,?,?,?,?,?,?,?);"
    PARAM1 = (data[1][0], data[1][1], data[0], data[1][2], data[1][3])
    PARAM2 = (data[0], data[2][0], data[2][1], data[2][2], 0, 0, 0, 0)
    PARAM3 = ([data[0]] + data[3])
    c.execute(QUERY1, PARAM1)
    c.execute(QUERY2, PARAM2)
    c.execute(QUERY3, PARAM3)
    conn.commit()
    conn.close()

# Deletes a user from the database
def remove_user(last_name, sid, osis):
    pass

# Checks if the user is an admin
def is_admin(username, password):
    conn = sqlite3.connect("super_secret.db")
    c = conn.cursor()
    QUERY = "SELECT * FROM admins WHERE username = ? AND password = ?;"
    result = list(c.execute(QUERY, (username, password)))
    conn.close()
    return len(result) == 1

