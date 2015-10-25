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
        "student_data"),(sid,)))[0][0]) == 1
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

# Gets a list of users provided a filter of fields
# The field of filters is a dictionary containing the keys:
# first_name_comparator         string that contains the beginning of the name
# last_name_comparator          string that contains the beginning of the name
# sid_comparator                string that contains the beginning of the sid
# osis_comparator               string that contains the beginning of the osis
# graduation_year               string that contains the graduation year
# safety_test                   boolean... duh
# team_dues                     boolean... duh
# medicals                      boolean... duh
# service_hours_lower           integer, lowerbound of service hours
# service_hours_upper           integer, upperbound of service hours
def get_data_with_filter(user_filter):
    first_name_comparator = user_filter['first_name'] + "%"
    last_name_comparator = user_filter['last_name'] + "%"
    sid_comparator = user_filter['sid'] + "%"
    osis_comparator = user_filter['osis'] + "%"
    graduation_year = user_filter['grad_year'] + "%"
    # If no value is given, assign a default one
    safety_test = user_filter.get("safety_test", False)
    team_dues = user_filter.get("dues", False)
    medicals = user_filter.get("medicals", False)
    service_hours_lower = 0 if not user_filter["service_hours_lower"] else user_filter["service_hours_lower"]
    service_hours_upper = 1000000 if not user_filter["service_hours_upper"] else user_filter["service_hours_upper"]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    QUERY1 = "SELECT sid FROM student_data WHERE sid LIKE ? AND \
        osis LIKE ? and grad_year LIKE ? AND safety_test = ? AND \
        team_dues = ? AND medicals = ? AND service_hours BETWEEN ? AND ?;"
    PARAM1 = (sid_comparator, osis_comparator, graduation_year, safety_test, team_dues, \
              medicals, service_hours_lower, service_hours_upper,)
    c.execute(QUERY1, PARAM1)
    sids = c.fetchall()

    QUERY2 = "SELECT first_name, last_name FROM students WHERE first_name LIKE ? AND last_name LIKE ? and sid LIKE ?;"
    PARAM2 = (first_name_comparator, last_name_comparator, sid_comparator,)

    # Format is {sid: (first_name, last_name,)}
    result = {}
    for sid in sids:
        sid = sid[0]
        c.execute(QUERY2, (first_name_comparator, last_name_comparator, sid,))
        result[sid] = c.fetchone()

    conn.close()
    return result

# Deletes a user from the database
def remove_user(last_name, sid, osis):
    if not user_exists(last_name, sid):
        return
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    QUERY1 = "DELETE FROM students WHERE last_name = ? AND sid = ?;"
    QUERY2 = "DELETE FROM student_data WHERE sid = ? AND osis = ?;"
    QUERY3 = "DELETE FROM parent_data WHERE sid = ?;"
    PARAM1 = (last_name, sid,)
    PARAM2 = (sid, osis,)
    PARAM3 = (sid,)
    c.execute(QUERY1, PARAM1)
    c.execute(QUERY2, PARAM2)
    c.execute(QUERY3, PARAM3)
    conn.commit()
    conn.close()

# Checks if the user is an admin
def is_admin(username, password):
    conn = sqlite3.connect("super_secret.db")
    c = conn.cursor()
    QUERY = "SELECT * FROM admins WHERE username = ? AND password = ?;"
    result = list(c.execute(QUERY, (username, password)))
    conn.close()
    return len(result) == 1

