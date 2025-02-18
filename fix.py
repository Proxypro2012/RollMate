from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

# Ensure CORS for development purposes
CORS(app)

# Path for the classdata file
CLASSDATA_FILE = 'classdata.txt'


# Utility function to ensure the file exists
def ensure_classdata_file():
    if not os.path.exists(CLASSDATA_FILE):
        with open(CLASSDATA_FILE, 'w') as file:
            pass  # Create an empty file if it doesn't exist


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


# D E B U G
if __name__ == '__main__':
    app.run(debug=True)
