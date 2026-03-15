import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    enrollment TEXT,
    dob TEXT
)
''')

# Sample Data
cursor.execute("INSERT INTO students (name, enrollment, dob) VALUES ('Rahul', '12345', '01-01-2005')")

conn.commit()
conn.close()