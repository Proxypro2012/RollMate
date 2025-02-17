from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from datetime import date, datetime
from kivy.core.window import Window
import subprocess
import platform
import requests
import json
import time
from kivy.uix.floatlayout import FloatLayout


# Color scheme
PRIMARY_COLOR = get_color_from_hex("#89CFF0")  # Green
SECONDARY_COLOR = get_color_from_hex("#2196F3")  # Blue
BACKGROUND_COLOR = get_color_from_hex("#FFFFFF")  # White
TEXT_COLOR = get_color_from_hex("#333333")  # Dark Gray

error_label = Label(
                text="",
                font_size="16sp",
                color=get_color_from_hex("#FF0000"),  # Red color for error,
                opacity=0
            )

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_color = (0, 0, 0, 0)  # Transparent
        self.background_normal = ""
        self.background_down = ""
        self.font_size = "18sp"
        self.bold = True
        self.color = BACKGROUND_COLOR
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*PRIMARY_COLOR)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20,])

    def on_press(self):
        anim = Animation(size=(self.width, self.height), duration=0.1)
        anim.start(self)

    def on_release(self):
        anim = Animation(size=(self.width, self.height), duration=0.1)
        anim.start(self)

class PeriodSelection(FloatLayout):  # Use FloatLayout here
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 40
        
        # Initialize selected_option to None
        self.selected_option = None
        
        self.add_widget(error_label)
        
        with self.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20,])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Position error_label higher
        error_label.pos_hint = {'center_x': 0.5, 'top': 0.85}  # Adjusted position
        
        # Period selection dropdown
        self.dropdown = DropDown(auto_width=False, width=200)
        for period in ['Period 1', 'Period 2', 'Period 3']:
            btn = RoundedButton(text=period, size_hint_y=None, height=50, pos_hint={'center_x': 0.5})
            btn.bind(on_release=lambda btn, period=period: self.update_button(self.main_button, period))
            self.dropdown.add_widget(btn)

        self.main_button = RoundedButton(text='Select Period', size_hint=(None, None), size=(200, 50))
        self.main_button.bind(on_release=self.dropdown.open)
        self.main_button.pos_hint = {'center_x': 0.5, 'top': 0.75}  # Position the dropdown above the sign-in button
        self.add_widget(self.main_button)

        # Sign-in button
        self.login_button = RoundedButton(text="Sign Me In", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'top': 0.5})
        self.add_widget(self.login_button)

        # Wi-Fi SSID label
        self.ssid_label = Label(text="Wi-Fi SSID will appear here.", font_size="16sp", color=TEXT_COLOR)
        self.ssid_label.pos_hint = {'center_x': 0.5, 'top': 0.9}
        self.add_widget(self.ssid_label)

        # Check Wi-Fi and bind login button
        wifi_name = self.get_wifi_name()
        if wifi_name == "SanjayTi":
            self.login_button.bind(on_press=self.on_login_button_press)
        else:
            self.login_button.bind(on_press=self.on_login_button_authen_error)

        # Update SSID label
        self.ssid_label.text = f"Connected to: {wifi_name}"

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_button(self, button, text):
        button.text = text
        self.selected_option = text
        print(f"Selected option: {self.selected_option}")
        self.dropdown.dismiss()

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
        # Check if selected_option is None or empty
        
        if not self.selected_option:
            errorlabeltext = "Please select a period before submitting attendance."
            error_label.text = str(errorlabeltext)
            error_label.opacity = 1
        
        wifi_name = self.get_wifi_name()
        current_date = date.today()
        current_time = datetime.now().time()

        # Load user data
        with open("user_data.txt", 'r') as f:
            user_data = f.read()
        
        first_name, last_name, user_id = self.extract_user_data(user_data)
        
        if self.selected_option == None:
            errorlabeltext = "Please select a period before submitting attendance."
            error_label.text = str(errorlabeltext)
            error_label.opacity = 1
        else:
            errorlabeltext = "Submitted!"
            error_label.text = str(errorlabeltext)
        
            attendance_data = {
                "userid": user_id,
                "networkName": wifi_name,
                "classname": self.selected_option,
                "date": current_date.strftime("%Y-%m-%d"),
                "firstName": first_name,
                "lastName": last_name,
                "checkinTime": current_time.strftime("%H:%M:%S")
            }

            url = "https://kabirtiwari.pythonanywhere.com/register"
            #url = "http://127.0.0.1:5000/register"
            response = requests.post(url, json=attendance_data)

            error_label.opacity = 1
            time.sleep(float(1))
            

            print(response.text)


    def on_login_button_authen_error(self, instance):
        errorlabeltext = "Invalid Connection: Try connecting to your school's internet connection."
        error_label.text = str(errorlabeltext)
        error_label.opacity = 1

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

class MyApp(App):
    def build(self):
        return PeriodSelection()

if __name__ == '__main__':
    Window.set_title("RollMate")
    MyApp().run()