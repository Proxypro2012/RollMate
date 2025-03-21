from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from datetime import datetime
import requests
import math
import json




# Color scheme
BASE_URL = "https://kabirtiwari.pythonanywhere.com"
#BASE_URL = "http://127.0.0.1:5000"
USER_DATA_FILE = "user_data.json"

PRIMARY_COLOR = get_color_from_hex("#89CFF0")
BACKGROUND_COLOR = get_color_from_hex("#FFFFFF")
TEXT_COLOR = get_color_from_hex("#333333")

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ""
        self.background_down = ""
        self.font_size = "18sp"
        self.color = TEXT_COLOR
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*PRIMARY_COLOR)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20, ])

class TeacherDashboard(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background setup
        with self.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, ])
        self.bind(pos=self.update_rect, size=self.update_rect)

        url = str(BASE_URL+'/get-classnames-by-teacher')

        with open(USER_DATA_FILE, 'r') as f:
            user_data = json.load(f)
        

        teacheruserId = user_data["user_id"]

        payload = {

            'teacherId': teacheruserId
        }

        response = requests.get(url, json=payload)

        data = response.json()
        print(data)
        classrooms = data["classnames"]



        # Title Label
        self.title_label = Label(
            text="Teacher Dashboard",
            font_size="24sp",
            color=TEXT_COLOR,
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        self.add_widget(self.title_label)

        # Class Selection Dropdown
        self.class_dropdown = DropDown(auto_width=False, width=200)
        for class_name in classrooms:
            btn = RoundedButton(text=class_name, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn, class_name=class_name: self.update_class_selection(btn.text))
            self.class_dropdown.add_widget(btn)

        self.class_button = RoundedButton(text="Select Class", size_hint=(None, None), size=(200, 50))
        self.class_button.bind(on_release=self.class_dropdown.open)
        self.class_button.pos_hint = {"center_x": 0.5, "top": 0.75}
        self.add_widget(self.class_button)

        
        self.attendance_label = Label(
            text="Enable Attendance",
            font_size="18sp",
            color=TEXT_COLOR,
            size_hint=(None, None),
            pos_hint={"center_x": 0.4, "top": 0.6}
        )
        self.add_widget(self.attendance_label)

        self.attendance_switch = Switch(
            active=False,
            size_hint=(None, None),
            size=(50, 30),
            pos_hint={"center_x": 0.6, "top": 0.6}
        )
        
        

        print(self.class_button.text)
        self.attendance_switch.bind(active=self.toggle_attendance)
        self.add_widget(self.attendance_switch)        
                
        
            



    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_class_selection(self, class_name):
        self.class_button.text = class_name

        url = str(BASE_URL+'/get-classroom-status')

        with open(USER_DATA_FILE, 'r') as f:
            user_data = json.load(f)
        

        teacheruserId = user_data["user_id"]

        payload = {

            'classname': self.class_button.text,
            'date': datetime.today().strftime('%Y-%m-%d')
        }

        response = requests.post(url, json=payload)
        
        data = response.json()
      
        classrooms = data["status"]

        if classrooms == "YES":
            self.attendance_switch.active = True
        else:
            self.attendance_switch.active = False

        self.class_dropdown.dismiss()
        print(f"Selected class: {class_name}")

    def toggle_attendance(self, instance, value):
        print("value:"+str(value))
        if value:
            self.attendance_label.text = "Disable Attendance"            
            url = str(BASE_URL+"/attendence-enable-switch-on")

            payload = {
                "status": "on",
                "classname": self.class_button.text,
                "date": datetime.now().strftime("%Y-%m-%d")
            }

            # Send request to server
            condition = payload["classname"]

            if not condition == "Select Class":
                response = requests.post(url, json=payload)
                print(response.text)
                print("Attendance Enabled")
            else:
                self.attendance_label.opacity = 1
                self.attendance_label.text = "Please Select a Classroom!"
                print("Please Select a Classroom!")
        else:
            self.attendance_label.text = "Enable Attendance"
            url = str(BASE_URL+"/attendence-enable-switch-off")
            payload = {
                "status": "off",
                "classname": self.class_button.text,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            
            condition = payload["classname"]

            if not condition == "Select Class":
                response = requests.post(url, json=payload)
                print(response.text)
                print("Attendance Disabled")
                
            else:
                self.attendance_label.opacity = 1
                self.attendance_label.text = "Please Select a Classroom!"
                print("Please Select a Classroom!")
                

class MyApp(App):

    def build(self):
        return TeacherDashboard()

if __name__ == '__main__':
    MyApp().run()
