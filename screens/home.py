from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from functools import partial  # ✅ Needed for proper event binding

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        # Background color setup
        with self.canvas.before:
            self.bg_color = Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_background, pos=self.update_background)

        # Main vertical layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # App logo
        layout.add_widget(Image(source='logo.png', size_hint=(1, 0.4), allow_stretch=True))

        # Scrollable area for buttons (useful on small screens)
        scroll = ScrollView(size_hint=(1, 0.6))
        btn_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        btn_container.bind(minimum_height=btn_container.setter('height'))

        buttons = [
            ('Add Safe Spot', 'add'),
            ('View Safe Spots', 'spots'),
            ('Emergency Contacts', 'emergency'),
            ('Events', 'events'),
            ('Settings', 'settings'),
            ('About', 'about'),
            ('Comments', 'comments'),
            ('Gallery', 'gallery')  # ✅ New screen for image gallery
        ]

        for text, screen_name in buttons:
            btn = Button(
                text=text,
                size_hint=(1, None),
                height='50dp',
                background_color=(0.95, 0.6, 0.4, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=partial(self.switch_screen, screen_name))  # ✅ Correct binding
            btn_container.add_widget(btn)

        scroll.add_widget(btn_container)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def switch_screen(self, screen_name, *args):  # ✅ Safe screen switch
        self.manager.current = screen_name