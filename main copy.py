from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import os
import subprocess
import platform
import requests
import json
from datetime import date
from datetime import datetime


USER_DATA_FILE = "user_data.txt"


class UserInfoPopup(Popup):
    def __init__(self, main_page, **kwargs):  # Pass the main page as an argument
        super(UserInfoPopup, self).__init__(**kwargs)
        self.main_page = main_page  # Store the main page reference
        self.title = "Enter Your Information"
        self.size_hint = (None, None)
        self.size = (600, 600)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Name input
        self.name_label = Label(text="First Name:")
        self.name_input = TextInput(multiline=False)
        layout.add_widget(self.name_label)
        layout.add_widget(self.name_input)
        
        # Last name input
        self.last_name_label = Label(text="Last Name:")
        self.last_name_input = TextInput(multiline=False)
        layout.add_widget(self.last_name_label)
        layout.add_widget(self.last_name_input)
        
        # User ID input
        self.user_id_label = Label(text="User ID:")
        self.user_id_input = TextInput(multiline=False)
        layout.add_widget(self.user_id_label)
        layout.add_widget(self.user_id_input)

        # Grade selection dropdown
        self.grade_level = None  # Variable to store selected grade level
        
        dropdown_for_grade_selection = DropDown()
        btn1 = Button(text='Grade 7', size_hint_y=None, height=44)
        btn2 = Button(text='Grade 8', size_hint_y=None, height=44)
        dropdown_for_grade_selection.add_widget(btn1)
        dropdown_for_grade_selection.add_widget(btn2)

        main_button_for_grade_selection = Button(text='Grade -->', size_hint=(None, None), height=44)
        main_button_for_grade_selection.bind(on_release=dropdown_for_grade_selection.open)
        btn1.bind(on_release=lambda btn: self.update_button(main_button_for_grade_selection, btn.text, dropdown_for_grade_selection))
        btn2.bind(on_release=lambda btn: self.update_button(main_button_for_grade_selection, btn.text, dropdown_for_grade_selection))

        layout.add_widget(main_button_for_grade_selection)

        # Submit button
        self.submit_button = Button(text="Submit")
        self.submit_button.bind(on_press=self.save_user_data)
        layout.add_widget(self.submit_button)

        self.add_widget(layout)
        

    def update_button(self, button, text, dropdown):
        button.text = text
        self.grade_level = text  # Store selected grade level
        print(f"Selected Grade Level: {self.grade_level}")
        dropdown.dismiss()

    def save_user_data(self, instance):
        # Get the input data
        first_name = self.name_input.text
        last_name = self.last_name_input.text
        user_id = self.user_id_input.text
        grade_level = self.grade_level
        
        # Print to see what we are getting from the text inputs
        print(f"First Name: {first_name}, Last Name: {last_name}, User ID: {user_id}, Grade Level: {self.grade_level}")

        # Store data in a file
        user_data = f"Name: {first_name} {last_name}\nUser ID: {user_id}\nGrade Level: {self.grade_level}"
        with open(USER_DATA_FILE, 'w') as f:
            f.write(user_data)

        # Add PeriodSelection widget to main page
        self.main_page.add_widget(PeriodSelection())

        self.dismiss()


class PeriodSelection(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create dropdown for selecting periods
        self.dropdown = DropDown()
        btn1 = Button(text='Period 1', size_hint_y=None, height=44)
        btn2 = Button(text='Period 2', size_hint_y=None, height=44)
        btn3 = Button(text='Period 3', size_hint_y=None, height=44)
        self.dropdown.add_widget(btn1)
        self.dropdown.add_widget(btn2)
        self.dropdown.add_widget(btn3)

        # Main button to trigger dropdown
        self.main_button = Button(text='Current class -->', size_hint=(None, None), height=44)
        self.main_button.bind(on_release=self.dropdown.open)
        btn1.bind(on_release=lambda btn: self.update_button(self.main_button, btn.text, self.dropdown))
        btn2.bind(on_release=lambda btn: self.update_button(self.main_button, btn.text, self.dropdown))
        btn3.bind(on_release=lambda btn: self.update_button(self.main_button, btn.text, self.dropdown))
        self.add_widget(self.main_button)

        # SSID label for displaying Wi-Fi name
        self.ssid_label = Label(
            text="Wi-Fi SSID will appear here.",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'x': 0.5, 'y': 0.3}
        )
        self.add_widget(self.ssid_label)

        # Login button
        self.login_button = Button(
            text="Sign Me In", 
            size_hint=(0.2, 0.2), 
            pos_hint={'x': 0.5, 'y': 0.5}
        )

        # Check if Wi-Fi name matches
        wifi_name = self.get_wifi_name()
        if wifi_name == "Shrewsbury":
            self.login_button.bind(on_press=self.on_login_button_press)
        else:
            self.login_button.bind(on_press=self.on_login_button_authen_error)
        self.add_widget(self.login_button)

    def update_button(self, button, text, dropdown):
        button.text = text
        self.selected_option = text
        print(f"Selected option: {self.selected_option}")
        dropdown.dismiss()

    def get_wifi_name(self):
        os_name = platform.system()
        try:
            if os_name == "Linux":
                wifi_name = subprocess.check_output(["iwgetid", "-r"]).decode("utf-8").strip()
                return wifi_name
            elif os_name == "Darwin":
                wifi_info = subprocess.check_output(["system_profiler", "SPAWiFiDataType"]).decode("utf-8")
                for line in wifi_info.splitlines():
                    if "SSID" in line:
                        return line.split(":")[1].strip()
            elif os_name == "Windows":
                wifi_name = subprocess.check_output("netsh wlan show interfaces", shell=True).decode("utf-8")
                for line in wifi_name.splitlines():
                    if "SSID" in line:
                        return line.split(":")[1].strip()
            else:
                return "Unsupported operating system."
        except subprocess.CalledProcessError:
            return "Could not retrieve Wi-Fi name. Are you connected to a Wi-Fi network?"

    def on_login_button_press(self, instance):
        wifi_name = self.get_wifi_name()
        current_date = date.today()
        current_time = datetime.now().time()

        # Load user data
        with open(USER_DATA_FILE, 'r') as f:
            user_data = f.read()
        
        first_name, last_name, user_id = self.extract_user_data(user_data)
        
        # Data as JSON
        attendance_data = {
            "userid": user_id,
            "networkName": wifi_name,
            "classname": self.selected_option,
            "date": current_date,
            "firstName": first_name,
            "lastName": last_name,
            "checkinTime": current_time
        }
        attendance_data["date"] = current_date.strftime("%Y-%m-%d")
        attendance_data["checkinTime"] = current_time.strftime("%H:%M:%S")

        json_payload = json.dumps(attendance_data)

        url = "https://kabirtiwari.pythonanywhere.com/register"
        response = requests.post(url, json=attendance_data)

        print(response.text)

    def on_login_button_authen_error(self, instance):
        error_label = Label(
            text="Error. Try connecting to your school's internet connection.",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'x': 0.5, 'y': 0.5}
        )
        self.add_widget(error_label)

    def extract_user_data(self, user_data):
        lines = [line.strip() for line in user_data.splitlines()]
        first_name, last_name = None, None
        if len(lines) > 0:
            name_line = lines[0].split(":")[1].strip()
            name_parts = name_line.split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""
        user_id = lines[1].split(":")[1].strip() if len(lines) > 1 else None
        return first_name, last_name, user_id


class MainPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not os.path.exists(USER_DATA_FILE):
            self.open_user_info_popup()
        else:
            self.add_widget(PeriodSelection())

    def open_user_info_popup(self):
        popup = UserInfoPopup(self)  # Pass the main page to the popup
        popup.open()


class MyApp(App):
    def build(self):
        return MainPage()


if __name__ == '__main__':
    MyApp().run()
