import streamlit as st
import requests

BASE_URL = "https://kabirtiwari.pythonanywhere.com"

st.title("Attendance UI")

# URL for attendance details
url = f"{BASE_URL}/attendencedetails"
response = requests.get(url=url)
data = response.json()

if not data:
    st.info("No attendance data available.")
else:
    # Extract unique values for filters
    network_names = list(set(entry['networkName'] for entry in data))
    class_names = list(set(entry['classname'] for entry in data))
    dates = list(set(entry['date'] for entry in data))
    usersid = list(set(entry['userid'] for entry in data))
    checkin_time = list(set(entry['checkinTime'] for entry in data))
    first_name = list(set(entry['firstName'] for entry in data))
    last_name = list(set(entry['lastName'] for entry in data))

    # Sidebar filters
    st.sidebar.header("Filters")
    selected_network = st.sidebar.selectbox("Select Network Name", ["All"] + network_names, key="network_name")
    selected_class = st.sidebar.selectbox("Select Class Name", ["All"] + class_names, key="class_name")
    selected_date = st.sidebar.selectbox("Select Date", ["All"] + dates, key="date")
    selected_userid = st.sidebar.selectbox("Select User ID", ["All"] + usersid, key="userid")
    selected_checkin_time = st.sidebar.selectbox("Select Checkin Time", ["All"] + checkin_time, key="checkin_time")
    selected_first_name = st.sidebar.selectbox("Select First Name", ["All"] + first_name, key="first_name")
    selected_last_name = st.sidebar.selectbox("Select Last Name", ["All"] + last_name, key="last_name")

    # Filter data based on selections
    filtered_data = [entry for entry in data if 
                     (selected_network == "All" or entry['networkName'] == selected_network) and
                     (selected_class == "All" or entry['classname'] == selected_class) and
                     (selected_date == "All" or entry['date'] == selected_date) and
                     (selected_userid == "All" or entry['userid'] == selected_userid) and
                     (selected_checkin_time == "All" or entry['checkinTime'] == selected_checkin_time) and
                     (selected_first_name == "All" or entry['firstName'] == selected_first_name) and
                     (selected_last_name == "All" or entry['lastName'] == selected_last_name)
    ]

    if not filtered_data:
        st.write("No matching records found.")
    else:
        # Create a table
        table_data = {
            "User ID": [entry['userid'] for entry in filtered_data],
            "Network Name": [entry['networkName'] for entry in filtered_data],
            "Class Name": [entry['classname'] for entry in filtered_data],
            "Date": [entry['date'] for entry in filtered_data],
            "First Name": [entry['firstName'] for entry in filtered_data],
            "Last Name": [entry['lastName'] for entry in filtered_data],
            "Checkin Time": [entry['checkinTime'] for entry in filtered_data]
        }

        # Display the dynamic table
        st.table(table_data)



    import streamlit as st
import requests

import streamlit as st
import requests

# Initialize session state variables
if "studentId" not in st.session_state:
    st.session_state.studentId = ""
if "newclass" not in st.session_state:
    st.session_state.newclass = ""
if "oldclass" not in st.session_state:
    st.session_state.oldclass = ""
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "show_change_class_form" not in st.session_state:
    st.session_state.show_change_class_form = False

# Sidebar button to trigger the form
#if st.sidebar.button("Add a new class"):
#    st.session_state.show_form = True
#    st.session_state.show_change_class_form = False   """# Hide change form if new class form is shown

if st.sidebar.button("Change class"):
    st.session_state.show_change_class_form = True
    st.session_state.show_form = False  # Hide new class form if change class form is shown

# Show form for adding a new class
if st.session_state.get("show_form", False):
    # Fetch data for student IDs
    student_ids = ["All"] + list(set(entry['userid'] for entry in data))  # Assuming `data` exists
    st.session_state.studentId = st.selectbox("Enter student id", options=student_ids)
    st.session_state.newclass = st.text_input("Enter new class name", value=st.session_state.newclass)

    if st.button("Submit"):
        if st.session_state.studentId and st.session_state.newclass:
            url = str(BASE_URL+"/add-new-class-by-student")
            payload = {
                "studentId": st.session_state.studentId,
                "newClass": st.session_state.newclass
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                st.success("New class added successfully.")
                st.session_state.show_form = False  # Hide the form after success
            else:
                st.error(f"Failed to add new class. Error: {response.text}")
        else:
            st.warning("Please enter student id and new class name.")

# Show form for changing an existing class
if st.session_state.get("show_change_class_form", False):
    # Fetch data for student IDs
    student_ids = ["All"] + list(set(entry['userid'] for entry in data))  # Assuming `data` exists
    st.session_state.studentId = st.selectbox("Enter student id", options=student_ids)
    st.session_state.oldclass = st.text_input("Enter old class name", value=st.session_state.oldclass)
    st.session_state.newclass = st.text_input("Enter new class name", value=st.session_state.newclass)

    if st.button("Submit"):
        if st.session_state.studentId and st.session_state.oldclass and st.session_state.newclass:
            url = str(BASE_URL+"/change-class-by-student")
            payload = {
                "studentId": st.session_state.studentId,
                "oldClass": st.session_state.oldclass,
                "newClass": st.session_state.newclass
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                st.success("Class changed successfully.")
                st.session_state.show_change_class_form = False  # Hide the form after success
            else:
                st.error(f"Failed to change class. Error: {response.text}")
        else:
            st.warning("Please enter student id, old class name, and new class name.")
