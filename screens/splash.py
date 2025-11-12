from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)

        # White background (guaranteed visible)
        Window.clearcolor = (1, 1, 1, 1)

        # Centered logo
        layout = AnchorLayout(anchor_x='center', anchor_y='center')

        # Use your logo file — put it in /storage/emulated/0/safespot/assets/
        logo = Image(
            source="assets/safespot_logo.png",
            size_hint=(0.6, 0.6),
            allow_stretch=True,
        )

        layout.add_widget(logo)
        self.add_widget(layout)

    def on_enter(self):
        # Go to login after 2.5 seconds
        Clock.schedule_once(self.switch_to_login, 2.5)

    def switch_to_login(self, dt):
        self.manager.transition.direction = "left"
        self.manager.current = "login"