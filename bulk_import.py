import sqlite3
import csv

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

with open('students.csv', 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute(
            "INSERT INTO students (name, enrollment, dob) VALUES (?, ?, ?)",
            (row['name'], row['enrollment'], row['dob'])
        )

conn.commit()
conn.close()

print("Bulk Data Imported Successfully!")