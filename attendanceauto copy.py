from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "Backend"








@app.route('/register', methods=['POST'])
def registration_page():
    classdata = request.get_json()
    if classdata is None:
        return jsonify({"error": "No JSON classdata provided :("}), 400

    userdetails = f"{classdata.get('userid')}\t{classdata.get('networkName')}\t{classdata.get('classname')}\t{classdata.get('date')}\t{classdata.get('firstName')}\t{classdata.get('lastName')}\t{classdata.get('checkinTime')}"

    with open('classdata.txt', 'a') as file:
        file.write(userdetails + "\n")

    print(classdata)
    return "classdata retrieved: Success! " + str(classdata)







@app.route('/attendencedetails', methods=['GET'])
def get_attendence_details():
    selected_rows = []

    # Read query parameters
    attendenceQuery = request.args  # Use query parameters (e.g., ?userid=1)
    print(f"Query parameters received: {attendenceQuery}")

    with open('classdata.txt', 'r') as file:
        attendencerows = file.readlines()

    # Use a set to track unique rows and remove duplicates
    unique_rows = set()
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

        # Convert the dictionary to a tuple (immutable) to check for uniqueness
        data_tuple = tuple(data.items())
        if data_tuple not in unique_rows:
            unique_rows.add(data_tuple)

            # Apply filtering based on query parameters (if provided)
            match = all(data.get(key) == value for key, value in attendenceQuery.items())
            if match:
                selected_rows.append(data)

    return jsonify(selected_rows)









@app.route('/get_classroom-by-teacher', methods=['GET'])
def get_classroom_by_teacher():
            data = request.get_json()
            if data is None:
                return jsonify({"error": "No JSON data provided :("}), 400

            teacher_id = data.get('teacher_id')
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

            return jsonify({"teacher_id": teacher_id, "classrooms": classrooms})







@app.route('/get_classroom-by-student', methods=['GET'])
def get_classroom_by_teacher():
            data = request.get_json()
            if data is None:
                return jsonify({"error": "No JSON data provided :("}), 400

            teacher_id = data.get('teacher_id')
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

            return jsonify({"teacher_id": teacher_id, "classrooms": classrooms})









if __name__ == '__main__':
    app.run(debug=True)






