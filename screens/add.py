import os
import json
import webbrowser

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup

from firebase_config import save_to_firebase


class AddSpotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title
        self.layout.add_widget(Label(text="Add a Safe Spot", font_size='26sp', size_hint=(1, None), height=50, color=(0.1, 0.1, 0.1, 1)))

        # Input fields
        self.name_input = TextInput(hint_text="Name", multiline=False, size_hint=(1, None), height=100, font_size='20sp')
        self.tag_input = TextInput(hint_text="Tag (e.g., Food, Shelter)", multiline=False, size_hint=(1, None), height=100, font_size='20sp')
        self.desc_input = TextInput(hint_text="Description", multiline=True, size_hint=(1, None), height=200, font_size='20sp')

        self.desc_char_label = Label(text="Max 500 characters", size_hint=(1, None), height=30, font_size='14sp', color=(0.3, 0.3, 0.3, 1))

        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.tag_input)
        self.layout.add_widget(self.desc_input)
        self.layout.add_widget(self.desc_char_label)

        # Submit button
        submit_btn = Button(text="Submit", size_hint=(1, None), height=60, background_color=(0.2, 0.6, 0.3, 1))
        submit_btn.bind(on_release=self.submit_spot)
        self.layout.add_widget(submit_btn)

        # Back button
        back_btn = Button(text="Back to Home", size_hint=(1, None), height=50, background_color=(0.5, 0.4, 0.3, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

        # Logo at the bottom
        self.logo = Image(source="logo.png", size_hint=(0.8, None), height=200, allow_stretch=True, keep_ratio=True)
        self.layout.add_widget(self.logo)

        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def submit_spot(self, instance):
        name = self.name_input.text.strip()
        tag = self.tag_input.text.strip()
        desc = self.desc_input.text.strip()

        if not name or not desc:
            self.show_popup("Error", "Name and description are required.")
            return

        spot = {"name": name, "tag": tag, "description": desc}
        if save_to_firebase("spots", spot):
            self.show_popup("Success", "Safe spot added successfully!")
            self.name_input.text = ""
            self.tag_input.text = ""
            self.desc_input.text = ""
        else:
            self.show_popup("Error", "Failed to save spot.")

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.7, 0.4))
        popup.open()