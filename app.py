from flask import Flask, render_template, request
import sqlite3
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# -------- DATABASE FUNCTION --------
def get_student(name):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT enrollment, dob FROM students WHERE name=?", (name,))
    data = cursor.fetchone()
    conn.close()
    return data


# -------- ASPX FETCH FUNCTION --------
def fetch_result(rollno, dob):

    session = requests.Session()
    url = "https://test.bteupexam.co.in/Odd_Semester/main/rollno.aspx"  # replace real URL

    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
    eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]
    viewstategenerator = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]

    payload = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": eventvalidation,
        "__VIEWSTATEGENERATOR": viewstategenerator,
        "txtRollNo": rollno,
        "txt_dob": dob,
        "btnSave": "Submit"
    }

    result_response = session.post(url, data=payload)

    return result_response.text


# -------- ROUTES --------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    student = get_student(name)

    if student:
        rollno, dob = student
        result_html = fetch_result(rollno, dob)
        return result_html

    return "Student not found"

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        enrollment = request.form['enrollment']
        dob = request.form['dob']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO students (name, enrollment, dob) VALUES (?, ?, ?)",
                       (name, enrollment, dob))

        conn.commit()
        conn.close()

        return "Student Added Successfully!"

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)