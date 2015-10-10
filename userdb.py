import sqlite3

db_name = "students.db"

def get_user(name, student_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    result = c.execute("SELECT * FROM %s WHERE name = %s AND sid = %s " % (db_name, name, student_id))
    if len(result) > 1:
        print("Strange things... multiple entries for: %s , %s" % (name, student_id));
        conn.close()
        return result[0]
    elif len(result) == 1:
        conn.close()
        return result[0]
    else:
        conn.close()
        return []

def check_user(name, student_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    result = c.execute("SELECT * FROM %s WHERE name = %s AND sid = %s " % (db_name, name, student_id))
    conn.close()
    if len(result) == 0:
        return 0 # No users found
    elif result[0] == "admin":
        return 2 # Cuz bigger number means bigger power :)
    else:
        return 1 # Normal user

def add_user(data):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "INSERT INTO " + db_name + " VALUES ("
    for item in data:
        if type(item) is str:
            query += "'%s'," % (item)
        elif type(item) is int:
            query += str(item) + ","
        else:
            query += ","
    query = query[:-1]
    query += ");"
    c.execute(query)
    c.commit()
    c.close()

