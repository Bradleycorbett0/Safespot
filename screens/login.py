import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

USERS_FILE = "/storage/emulated/0/safespot/users.json"
Window.softinput_mode = 'resize'

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_background, pos=self.update_background)

        root = FloatLayout()

        layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=30,
            size_hint=(0.9, 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )

        layout.add_widget(Label(
            text="Login to SafeSpot",
            font_size='30sp',
            size_hint=(1, None),
            height=50,
            color=(0.2, 0.2, 0.2, 1)
        ))

        self.email_input = TextInput(
            hint_text="Email or Phone",
            multiline=False,
            font_size='22sp',
            size_hint=(1, None),
            height=95
        )
        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            font_size='22sp',
            size_hint=(1, None),
            height=95
        )

        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)

        login_btn = Button(
            text="Login",
            size_hint=(1, None),
            height=65,
            background_color=(0.2, 0.4, 0.2, 1),
            font_size='20sp'
        )
        login_btn.bind(on_press=self.handle_login)
        layout.add_widget(login_btn)

        register_btn = Button(
            text="Register",
            size_hint=(1, None),
            height=65,
            background_color=(0.25, 0.2, 0.35, 1),
            font_size='20sp'
        )
        register_btn.bind(on_press=self.handle_register)
        layout.add_widget(register_btn)

        root.add_widget(layout)

        logo = Image(
            source="logo.png",
            size_hint=(0.6, 0.25),
            pos_hint={"center_x": 0.5, "y": 0.01}
        )
        root.add_widget(logo)

        self.add_widget(root)

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def handle_login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        users = self.load_users()
        if any(user.get("email") == email and user.get("password") == password for user in users):
            self.manager.current = "permission"
        else:
            self.show_popup("Login Failed", "Incorrect email or password.")

    def handle_register(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        users = self.load_users()

        if any(user.get("email") == email for user in users):
            self.show_popup("Error", "Account already exists.")
            return

        users.append({'email': email, 'password': password})
        self.save_users(users)
        self.show_popup("Success", "Account created.")

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.75, 0.4)
        )
        popup.open()

    def load_users(self):
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        return []

    def save_users(self, users):
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)