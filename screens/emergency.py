# emergency.py
import os
import json
import webbrowser
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior

CONTACTS_FILE = "/storage/emulated/0/safespot/emergency_contacts.json"

class ClickableLabel(ButtonBehavior, Label):
    pass

class EmergencyContactsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.scrollview = ScrollView()
        self.contact_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=20, padding=(10, 10))
        self.contact_list.bind(minimum_height=self.contact_list.setter('height'))
        self.scrollview.add_widget(self.contact_list)
        self.layout.add_widget(self.scrollview)

        add_btn = Button(
            text="Add Emergency Contact",
            size_hint=(1, None),
            height=50,
            background_color=(0.1, 0.4, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        add_btn.bind(on_release=self.show_add_popup)
        self.layout.add_widget(add_btn)

        back_btn = Button(
            text="Back to Home",
            size_hint=(1, None),
            height=50,
            background_color=(0.3, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self):
        self.load_contacts()

    def load_contacts(self):
        self.contact_list.clear_widgets()
        if not os.path.exists(CONTACTS_FILE):
            return

        with open(CONTACTS_FILE, "r") as f:
            contacts = json.load(f)

        for contact in contacts:
            name = contact.get("name", "Unnamed")
            value = contact.get("phone", "")

            container = BoxLayout(orientation='vertical', size_hint_y=None, height=60, padding=(10, 5))

            display_text = f"[u]{name}[/u]: {value if value else 'N/A'}"
            label = ClickableLabel(
                text=display_text,
                markup=True,
                halign='center',
                valign='middle',
                size_hint_y=None,
                height=50,
                font_size='16sp',
                color=(0.1, 0.1, 0.5, 1)
            )
            label.bind(size=lambda lbl, val: setattr(lbl, 'text_size', (lbl.width - 20, None)))

            if value.startswith("http"):
                label.bind(on_press=lambda inst, url=value: webbrowser.open(url))
            elif value.isdigit():
                label.bind(on_press=lambda inst, number=value: webbrowser.open(f"tel:{number}"))

            container.add_widget(label)
            self.contact_list.add_widget(container)

    def show_add_popup(self, instance):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        name_input = TextInput(hint_text="Name", multiline=False)
        phone_input = TextInput(hint_text="Phone Number or URL", multiline=False)

        save_btn = Button(text="Save", size_hint=(1, None), height=40)
        cancel_btn = Button(text="Cancel", size_hint=(1, None), height=40)

        box.add_widget(name_input)
        box.add_widget(phone_input)
        box.add_widget(save_btn)
        box.add_widget(cancel_btn)

        popup = Popup(title="Add Contact", content=box, size_hint=(0.9, 0.6))

        def save_contact(instance):
            name = name_input.text.strip()
            phone = phone_input.text.strip()
            if name and phone:
                self.save_contact(name, phone)
                popup.dismiss()
                self.load_contacts()

        save_btn.bind(on_release=save_contact)
        cancel_btn.bind(on_release=popup.dismiss)
        popup.open()

    def save_contact(self, name, phone):
        contacts = []
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as f:
                contacts = json.load(f)

        contacts.append({"name": name, "phone": phone})

        with open(CONTACTS_FILE, "w") as f:
            json.dump(contacts, f, indent=2)