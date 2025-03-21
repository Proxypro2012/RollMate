from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation

class CustomCursorLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(CustomCursorLayout, self).__init__(**kwargs)
        
        # Hide default cursor
        Window.show_cursor = False
        
        # Create custom cursor
        self.cursor = Image(source='custom_cursor.png', allow_stretch=True, keep_ratio=False)
        self.cursor.opacity = 0.8  # Make it more visible
        self.cursor.size_hint = (None, None)
        self.cursor.size = (20, 20)  # Adjust size as needed
        self.add_widget(self.cursor)
        
        # Update cursor position continuously
        Clock.schedule_interval(self.update_cursor_position, 1 / 960.0)
        
        # Smoothing factor for interpolation
        self.ease_factor = 0.08  # Lower value = slower easing
        
    def update_cursor_position(self, dt):
        # Get current and target mouse positions
        current_x, current_y = self.cursor.pos
        target_x, target_y = Window.mouse_pos[0] - self.cursor.width / 2, Window.mouse_pos[1] - self.cursor.height / 2

        # Interpolation (Ease-in effect)
        new_x = current_x + (target_x - current_x) * self.ease_factor
        new_y = current_y + (target_y - current_y) * self.ease_factor

        self.cursor.pos = (new_x, new_y)

        # Animation for smoother effect (Optional)
        anim = Animation(pos=(new_x, new_y), duration=0.05, t='in_quad')
        anim.start(self.cursor)
        
class CustomCursorApp(App):
    def build(self):
        return CustomCursorLayout()

if __name__ == '__main__':
    CustomCursorApp().run()
