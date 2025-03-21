from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from teacher_dashboard import TeacherDashboard
import os
import subprocess
import platform
import requests
import json
from datetime import date
from datetime import datetime
from kivy.core.window import Window
from student_dashboard import StudentDashboard   # Imports Seperated Class (Vital!)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
import subprocess
import platform
import requests
import json
from datetime import date, datetime
import math 
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.clock import Clock







USER_DATA_FILE = "user_data.json"


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window






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

        # Portal selection switch
        self.portal_label = Label(text="Select Portal:")
        layout.add_widget(self.portal_label)

        self.portal_switch = BoxLayout(orientation='horizontal', size_hint=(1, None), height=44)
        self.portal_option_label = Label(text="Student", size_hint=(0.7, 1))  # Default to "Student"
        self.switch = Switch(active=False)  # Default is "Student" (off state)
        self.switch.bind(active=self.on_switch_active)

        self.portal_switch.add_widget(self.portal_option_label)
        self.portal_switch.add_widget(self.switch)
        layout.add_widget(self.portal_switch)

        # Submit button
        self.submit_button = Button(text="Submit")
        self.submit_button.bind(on_press=self.save_user_data)
        layout.add_widget(self.submit_button)

        self.add_widget(layout)
        
    def update_button(self, button, text, dropdown):
        button.text = text
        self.grade_level = text  # Store selected grade level
        print(f"Selected Grade Level: {self.grade_level}")
        print("Main")
        dropdown.dismiss()

    def on_switch_active(self, instance, value):
        if value:
            self.portal_option_label.text = "Teacher"
        else:
            self.portal_option_label.text = "Student"
        print(f"Portal selected: {self.portal_option_label.text}")

    def save_user_data(self, instance):
        # Get the input data
        first_name = self.name_input.text
        last_name = self.last_name_input.text
        user_id = self.user_id_input.text
        grade_level = self.grade_level
        portal = self.portal_option_label.text.lower()  # Convert "Student"/"Teacher" to lowercase
        

        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "user_id": user_id,
            "grade_level": grade_level,
            "portal": portal
        }


        # Print to see what we are getting from the text inputs
        print(f"First Name: {first_name}, Last Name: {last_name}, User ID: {user_id}, Grade Level: {grade_level}, Portal: {portal}")

        # Store data in a file
        # user_data = f"Name: {first_name} {last_name}\nUser ID: {user_id}\nGrade Level: {grade_level}\nProfile: {portal}"
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(user_data, f, indent=4)

    
        if portal == "student":
                student_dashboard = StudentDashboard()
                self.main_page.add_widget(student_dashboard)
                #apply_custom_cursor(student_dashboard)
        if portal == "teacher":
                teacher_dashboard = TeacherDashboard()
                self.main_page.add_widget(teacher_dashboard)
                #apply_custom_cursor(TeacherDashboard())

        

        self.dismiss()







""" class CustomCursor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor = Image(source="custom_cursor.png", size_hint=(None, None), size=(22, 22))
        self.add_widget(self.cursor)
        self.cursor.opacity = 0.5
        Window.bind(mouse_pos=self.update_cursor_pos)
        Window.show_cursor = False  # Hide system cursor

    def update_cursor_pos(self, window, pos):
        with canvas.after:
            self.cursor.pos = (pos[0] - 16, pos[1] - 16)  # Adjust based on cursor size

# This function ensures the cursor is added globally
def apply_custom_cursor(root_widget):
    if not hasattr(root_widget, "cursor_added"):  # Prevent duplicate cursors
        cursor = CustomCursor()
        root_widget.add_widget(cursor)
        root_widget.cursor_added = True """







class MainPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #apply_custom_cursor(self)
    
        Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background
        
        
       
        if not os.path.exists(USER_DATA_FILE):
            self.open_user_info_popup()
        else:
            with open(USER_DATA_FILE, 'r') as f:
                user_data = json.load(f)
            profile = user_data.get("portal", "student")
            if profile == "student":
                student_dashboard = StudentDashboard()
                self.add_widget(student_dashboard)
                #apply_custom_cursor(student_dashboard)
            if profile == "teacher":
                teacher_dashboard = TeacherDashboard()
                self.add_widget(teacher_dashboard)
                #apply_custom_cursor(teacher_dashboard)

    def open_user_info_popup(self):
        popup = UserInfoPopup(self)  # Pass the main page to the popup
        popup.open()




class RollMate(App):
    def build(self):
        return MainPage()



if __name__ == '__main__':
    Window.set_title("RollMate")
    Window.set_icon('logo.png')
    RollMate().run()


    