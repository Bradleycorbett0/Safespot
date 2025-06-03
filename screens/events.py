import os
import json

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

EVENTS_FILE = "events.json"

class EventsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        self.scrollview = ScrollView(size_hint=(1, 0.75))
        self.content = GridLayout(cols=1, size_hint_y=None, padding=[10, 10], spacing=20)
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scrollview.add_widget(self.content)
        self.layout.add_widget(self.scrollview)

        button_bar = BoxLayout(size_hint=(1, 0.1), spacing=10)
        add_btn = Button(text='Add', background_color=(0.3, 0.6, 0.4, 1))
        del_btn = Button(text='Delete', background_color=(0.8, 0.4, 0.4, 1))
        add_btn.bind(on_press=self.open_add_popup)
        del_btn.bind(on_press=self.open_delete_popup)
        button_bar.add_widget(add_btn)
        button_bar.add_widget(del_btn)
        self.layout.add_widget(button_bar)

        back_btn = Button(text='Back to Home', size_hint=(1, 0.1), background_color=(0.95, 0.6, 0.4, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self, *args):
        self.refresh_events()

    def refresh_events(self):
        self.content.clear_widgets()
        events = self.load_events()
        for event in events:
            label = Label(
                text=event,
                font_size='22sp',
                color=(0.2, 0.2, 0.2, 1),
                size_hint_y=None,
                halign='left',
                valign='middle',
                text_size=(self.width - 60, None),
                height=0  # Auto-size
            )
            label.bind(
                texture_size=lambda inst, size: setattr(inst, 'height', max(size[1], 50))
            )
            self.content.add_widget(label)

    def open_add_popup(self, instance):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)

        input_field = TextInput(
            hint_text='Enter new event',
            multiline=True,
            size_hint_y=0.7,
            font_size='20sp',
            background_color=(1, 0.98, 0.94, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10, 10, 10]
        )
        box.add_widget(input_field)

        def save_event(instance):
            new_event = input_field.text.strip()
            if new_event:
                events = self.load_events()
                events.append(new_event)
                self.save_events(events)
                self.refresh_events()
            popup.dismiss()

        save_btn = Button(text="Save", background_color=(0.3, 0.6, 0.4, 1), size_hint_y=0.3)
        save_btn.bind(on_press=save_event)
        box.add_widget(save_btn)

        popup = Popup(title="Add Event", content=box, size_hint=(0.9, 0.5))
        popup.open()

    def open_delete_popup(self, instance):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)

        input_field = TextInput(
            hint_text='Enter exact event text to delete',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size='18sp',
            background_color=(1, 0.98, 0.94, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10, 10, 10]
        )
        box.add_widget(input_field)

        def delete_event(instance):
            to_delete = input_field.text.strip()
            if to_delete:
                events = self.load_events()
                if to_delete in events:
                    events.remove(to_delete)
                    self.save_events(events)
                    self.refresh_events()
            popup.dismiss()

        delete_btn = Button(text="Delete", background_color=(0.8, 0.4, 0.4, 1), size_hint_y=0.3)
        delete_btn.bind(on_press=delete_event)
        box.add_widget(delete_btn)

        popup = Popup(title="Delete Event", content=box, size_hint=(0.9, 0.4))
        popup.open()

    def load_events(self):
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, "r") as f:
                return json.load(f)
        return []

    def save_events(self, events):
        with open(EVENTS_FILE, "w") as f:
            json.dump(events, f, indent=2)