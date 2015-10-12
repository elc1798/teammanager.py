import sqlite3

db_name = "users.db"

conn = sqlite3.connect(db_name)
c = conn.cursor()
c.execute("CREATE TABLE students (last_name text, first_name text, sid text,\
email text, cell integer);")
c.execute("CREATE TABLE student_data (sid text, osis integer, DOB text,\
grad_year integer, safety_test integer, team_dues integer, service_hours integer);")
c.execute("CREATE TABLE parent_data (sid text, mother text, father text,\
mother_email text, father_email text, home_phone integer, mother_cell integer,\
father_cell, pref_lang text);")

conn.commit()
conn.close()

