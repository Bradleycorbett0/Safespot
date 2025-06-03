from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class PermissionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_background, pos=self.update_background)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        layout.add_widget(Label(
            text="Please grant permissions to use the app.",
            font_size='20sp',
            color=(0.2, 0.2, 0.2, 1)
        ))

        grant_btn = Button(
            text="Grant Permissions",
            size_hint=(1, 0.2),
            background_color=(0.3, 0.6, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        grant_btn.bind(on_release=self.grant_permissions)
        layout.add_widget(grant_btn)

        self.add_widget(layout)

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def grant_permissions(self, *args):
        # Just switch to home screen for now
        self.manager.current = 'home'