from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
import webbrowser
import os

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title
        title = Label(
            text="About SafeSpot",
            font_size='22sp',
            bold=True,
            size_hint_y=None,
            height=40,
            color=(0, 0, 0, 1)
        )
        layout.add_widget(title)

        # Scrollable info
        scroll = ScrollView(size_hint=(1, 0.6))

        self.info = Label(
            text=(
                "SafeSpot helps you find safe, welcoming places nearby.\n\n"
                "Our mission is to make you feel safer and more supported in your community.\n\n"
                "We use ads to keep this app free. Your ad preferences are stored locally.\n"
                "You can review our privacy policy below."
            ),
            halign='center',
            valign='top',
            size_hint_y=None,
            markup=True,
            color=(0, 0, 0, 1),
        )
        self.info.bind(texture_size=self.update_label_height)
        scroll.add_widget(self.info)
        layout.add_widget(scroll)

        # Privacy button
        privacy_btn = Button(
            text="View Privacy Policy",
            size_hint_y=None,
            height=50,
            background_color=(0, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
        )
        privacy_btn.bind(on_release=lambda x: webbrowser.open("file://" + os.path.abspath("privacy_policy.html")))

        # Back button
        back_btn = Button(
            text="Back",
            size_hint_y=None,
            height=50,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
        )
        back_btn.bind(on_release=self.go_home)

        layout.add_widget(privacy_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)
        self.bind(size=self.update_text_size)

    def update_label_height(self, instance, size):
        instance.height = size[1]

    def update_text_size(self, *args):
        self.info.text_size = (self.width - 40, None)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def go_home(self, instance):
        self.manager.current = 'home'