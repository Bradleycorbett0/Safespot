import json
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation

# Pre-initialize window color (prevents black screen *before* splash)
Window.clearcolor = (1, 1, 1, 1)

# --- Import your existing screens ---
from screens.login import LoginScreen
from screens.permission import PermissionScreen
from screens.home import HomeScreen
from screens.add import AddSpotScreen
from screens.spots import SpotsScreen
from screens.emergency import EmergencyContactsScreen
from screens.events import EventsScreen
from screens.settings import SettingsScreen
from screens.about import AboutScreen
from screens.comments import CommentsScreen
from screens.gallery import ImageGalleryScreen
from screens.adpermission import AdPermissionScreen


# --- Splash Screen ---
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)

        # White background for the splash
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Centered SafeSpot logo
        self.layout = AnchorLayout(anchor_x="center", anchor_y="center")
        self.logo = Image(
            source="assets/safespot_logo.png",
            allow_stretch=True,
            size_hint=(0.5, 0.5),
            opacity=0
        )
        self.layout.add_widget(self.logo)
        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def on_enter(self):
        # Fade-in then fade-out logo
        fade_in = Animation(opacity=1, duration=0.9)
        fade_out = Animation(opacity=0, duration=0.7)
        fade_in.bind(on_complete=lambda *x: fade_out.start(self.logo))
        fade_out.bind(on_complete=lambda *x: self.go_to_login())
        fade_in.start(self.logo)

    def go_to_login(self, *args):
        self.manager.transition = NoTransition()
        self.manager.current = "login"


# --- Main App ---
class SafeSpotApp(App):
    def build(self):
        self.title = "SafeSpot"
        self.logged_in = False
        self.data_file = os.path.join(self.user_data_dir, "userdata.json")

        sm = ScreenManager(transition=NoTransition())

        # Add splash first
        sm.add_widget(SplashScreen(name="splash"))

        # Add all existing screens
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(PermissionScreen(name="permission"))
        sm.add_widget(AdPermissionScreen(name="adpermission"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(AddSpotScreen(name="add"))
        sm.add_widget(SpotsScreen(name="spots"))
        sm.add_widget(EmergencyContactsScreen(name="emergency"))
        sm.add_widget(EventsScreen(name="events"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(AboutScreen(name="about"))
        sm.add_widget(CommentsScreen(name="comments"))
        sm.add_widget(ImageGalleryScreen(name="gallery"))

        sm.current = "splash"
        return sm

    def save_user_data(self, key, value):
        data = self.load_user_data()
        if not isinstance(data, dict):
            data = {}
        data[key] = value
        try:
            with open(self.data_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def load_user_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except Exception as e:
                print(f"Error loading user data: {e}")
                return {}
        return {}


if __name__ == "__main__":
    SafeSpotApp().run()