from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from flask import Flask, session, request, redirect, url_for, render_template, flash


app = Flask(__name__)


# Ensure CORS for development purposes
CORS(app)

global_session_data = {}

#app.config['SESSION_TYPE'] = 'filesystem'  # Other options: 'redis', 'memcached', 'mongodb', etc.
#app.config['SECRET_KEY'] = 'your_secret_key'  # Required for signing the session cookie



# Path for the classdata file
CLASSDATA_FILE = 'classdata.txt'


# Utility function to ensure the file exists
def ensure_classdata_file():
    if not os.path.exists(CLASSDATA_FILE):
        with open(CLASSDATA_FILE, 'w') as file:
            pass  # Create an empty file if it doesn't exist



def set_attendence_key(key, value):
    global_session_data[key] = value
    print("Value Has Been Set")


def get_attencence_value(key):
    value = global_session_data.get(key, 'NO')
    return value





@app.route('/')
def home():
    return "Backend"








@app.route('/register', methods=['POST'])
def registration_page():
    # Ensure the classdata file exists
    ensure_classdata_file()

    classdata = request.get_json()
    if classdata is None:
        return jsonify({"error": "No JSON classdata provided :("}), 400

    userdetails = f"{classdata.get('userid')}\t{classdata.get('networkName')}\t{classdata.get('classname')}\t{classdata.get('date')}\t{classdata.get('firstName')}\t{classdata.get('lastName')}\t{classdata.get('checkinTime')}"

    # Append data to the classdata file
    with open(CLASSDATA_FILE, 'a') as file:
        file.write(userdetails + "\n")

    print(classdata)
    return "classdata retrieved: Success! " + str(classdata)








@app.route('/attendencedetails', methods=['GET'])
def get_attendence_details():
    # Ensure the classdata file exists
    ensure_classdata_file()

    selected_rows = []

    # Read query parameters
    attendenceQuery = request.args  # Use query parameters (e.g., ?userid=1)
    print(f"Query parameters received: {attendenceQuery}")

    with open(CLASSDATA_FILE, 'r') as file:
        attendencerows = file.readlines()

    # Dictionary to track unique rows without considering check-in time
    unique_records = {}

    for line in attendencerows:
        fields = line.strip().split("\t")
        if len(fields) != 7:  # Ensure the line has all required fields
            continue
        data = {
            "userid": fields[0],
            "networkName": fields[1],
            "classname": fields[2],
            "date": fields[3],
            "firstName": fields[4],
            "lastName": fields[5],
            "checkinTime": fields[6],
        }

        # Create a key excluding check-in time
        unique_key = (data["userid"], data["networkName"], data["classname"], data["date"], data["firstName"], data["lastName"])

        # Store only the first occurrence of each unique key
        if unique_key not in unique_records:
            unique_records[unique_key] = data

    # Apply filtering based on query parameters (if provided)
    for record in unique_records.values():
        match = all(record.get(key) == value for key, value in attendenceQuery.items())
        if match:
            selected_rows.append(record)

    return jsonify(selected_rows)




@app.route('/attendence-enable-switch-on', methods=['POST'])
def toggle_attendance_enable_switch_on():
    data = request.get_json()
    unique_records = data['classname'] + ":" + data['date']

    attendencevalue = get_attencence_value(unique_records)
    if attendencevalue == 'NO':
        set_attendence_key(unique_records, 'YES')
        return jsonify({"message": "Attendance Enabled"})
    else:
        return jsonify({"message": "Attendance Already Enabled"})
    





@app.route('/attendence-enable-switch-off', methods=['POST'])
def toggle_attendance_enable_switch_off():
    data = request.get_json()
    unique_records = data['classname'] + ":" + data['date']

    attendencevalue = get_attencence_value(unique_records)
    if attendencevalue == 'YES':
        set_attendence_key(unique_records, 'NO')
        return jsonify({"message": "Attendance Disabled"})
    else:
        return jsonify({"message": "Attendance Already Disabled"})







@app.route('/get-classroom-status', methods=['POST'])
def get_attendence_status():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    print(data)
    unique_records = data['classname'] + ":" + data['date']
    attendencevalue = get_attencence_value(unique_records)
    return jsonify({"status": attendencevalue})







@app.route('/get-classnames-by-teacher', methods=['GET'])
def get_classnames_by_teacher():
            data = request.get_json()
            if data is None:
                return jsonify({"error": "No JSON data provided :("}), 400

            teacher_id = data.get('teacherId')
            if not teacher_id:
                return jsonify({"error": "No teacher_id provided :("}), 400

            classrooms = []
            with open('teachers_classroom.tsv', 'r') as file:
                for line in file:
                    fields = line.strip().split("\t")
                    if len(fields) != 2:  # Ensure the line has all required fields
                        continue
                    if fields[0] == teacher_id:
                        classrooms.append(fields[1])

            return jsonify({"teacherId": teacher_id, "classnames": classrooms})







@app.route('/get-classnames-by-student', methods=['GET'])
def get_classnames_by_student():
            data = request.get_json()
            if data is None:
                return jsonify({"error": "No JSON data provided :("}), 400

            student_id = data.get('studentId')
            if not student_id:
                return jsonify({"error": "No teacher_id provided :("}), 400

            classrooms = []
            with open('students_classroom.tsv', 'r') as file:
                for line in file:
                    fields = line.strip().split("\t")
                    if len(fields) != 2:  # Ensure the line has all required fields
                        continue
                    if fields[0] == student_id:
                        classrooms.append(fields[1])

            return jsonify({"studentId": student_id, "classnames": classrooms})












# D E B U G
if __name__ == '__main__':
    app.run(debug=True)

