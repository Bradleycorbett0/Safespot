from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.window import Window
import json
import os


# Make window auto-resize when keyboard opens
try:
    Window.softinput_mode = "pan"  # 'pan' moves content up when keyboard shows
except Exception as e:
    print("Keyboard resize mode not set:", e)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Background
        self.background_color = (0.98, 0.95, 0.9, 1)

        # Use a ScrollView to prevent hiding content
        scroll = ScrollView(size_hint=(1, 1))

        container = BoxLayout(
            orientation="vertical",
            padding=[40, 60, 40, 60],
            spacing=20,
            size_hint_y=None
        )
        container.bind(minimum_height=container.setter("height"))

        # Title / logo
        logo_label = Label(
            text="[b]SafeSpot[/b]",
            markup=True,
            font_size="36sp",
            color=(0, 0.4, 0.4, 1),
            size_hint_y=None,
            height=dp(60)
        )

        # Subtitle
        self.subtitle = Label(
            text="Find safety. Feel supported.",
            font_size="16sp",
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )

        # Username
        self.username_input = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[15, 15],
            cursor_color=(0, 0.4, 0.4, 1)
        )

        # Password
        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[15, 15],
            cursor_color=(0, 0.4, 0.4, 1)
        )

        # Login button
        self.login_button = Button(
            text="Login",
            size_hint_y=None,
            height=dp(50),
            background_color=(0, 0.4, 0.4, 1),
            color=(1, 1, 1, 1),
            font_size="18sp",
            bold=True
        )
        self.login_button.bind(on_press=self.login)

        # Skip button
        self.skip_button = Button(
            text="Skip Login",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            font_size="16sp"
        )
        self.skip_button.bind(on_press=self.skip_login)

        # Add widgets
        container.add_widget(logo_label)
        container.add_widget(self.subtitle)
        container.add_widget(self.username_input)
        container.add_widget(self.password_input)
        container.add_widget(self.login_button)
        container.add_widget(self.skip_button)

        scroll.add_widget(container)

        # Use anchor layout to center scroll area
        root = AnchorLayout(anchor_x="center", anchor_y="center")
        root.add_widget(scroll)
        self.add_widget(root)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.subtitle.text = "[color=ff0000]Please fill in both fields[/color]"
            self.subtitle.markup = True
            return

        data_file = os.path.join(os.path.expanduser("~"), "safespot_userdata.json")
        data = {"username": username}

        try:
            with open(data_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving user data: {e}")

        self.manager.current = "home"

    def skip_login(self, instance):
        self.manager.current = "home"