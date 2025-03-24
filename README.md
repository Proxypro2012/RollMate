# RollMate
A mobile application created for schools and institutions to Automate their attendance systems.



My middle school's attendance system is really outdated and inefficient. Teachers and assistants will go through the **Schoology Attendance Portal**, marking us either 'present' or 'absent' depending on our status. 
RollMate is here to simplify and automate this problem, by sending API requests to schoology's attendance endpoint with the details of the user of the app. Teachers won't have to go through each student manually and check them off as my app will cover this.



![Screenshot 2025-03-23 123140](https://github.com/user-attachments/assets/d3fc28d2-09d3-47c2-ac07-f50e43dd6533)

***(Some basic user data being stored in a .json file)***
 
 
 
 
 
 
 
My app uses **Kivy**, a comprehensive python library built for developing cross platform apps in pure python.
To get started, simply run:

(On Windows) - 
`pip install kivy `

(On Mac) - 
`pip3 install kivy`







I have a flask powered API server running in the background, hosted on **Anaconda's PythonAnywhere**, a great free site for hosting python servers.
My server is temporary, but it is powered by many different requests. For example:


'''   
       
    
       # Utility function to ensure the file exists
      def ensure_classdata_file():
           if not os.path.exists(CLASSDATA_FILE):
               with open(CLASSDATA_FILE, 'w') as file:
                   pass  # Create an empty file if it doesn't exist
       


      @app.route('/attendencedetails', methods=['GET'])
      def get_attendence_details():
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
'''
