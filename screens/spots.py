import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


class SafeSpotsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background color
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Scrollable spot list
        self.scrollview = ScrollView()
        self.spot_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        self.spot_list.bind(minimum_height=self.spot_list.setter('height'))
        self.scrollview.add_widget(self.spot_list)
        self.layout.add_widget(self.scrollview)

        # Back button
        back_btn = Button(
            text='Back to Home',
            size_hint=(1, 0.1),
            background_color=(0.6, 0.4, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self):
        self.refresh_spots()

    def refresh_spots(self):
        self.spot_list.clear_widgets()

        spots_file = "/storage/emulated/0/safespot/saved_spots.json"
        if not os.path.exists(spots_file):
            self.spot_list.add_widget(Label(text="No spots saved yet.", size_hint_y=None, height=40))
            return

        try:
            with open(spots_file, "r") as f:
                spots = json.load(f)

            for spot in sorted(spots, key=lambda x: x.get('name', '').lower()):
                name = spot.get('name', 'Unnamed')
                tag = spot.get('tag', '')
                desc = spot.get('description', '')

                full_text = f"[b]{name}[/b] ({tag})\n{desc}"

                lbl = Label(
                    text=full_text,
                    markup=True,
                    size_hint_y=None,
                    halign='left',
                    valign='top',
                    font_size='16sp',
                    color=(0.1, 0.1, 0.1, 1)
                )

                # Bind width and update text layout
                def update_label(instance, value):
                    instance.text_size = (value - 40, None)
                    instance.texture_update()
                    instance.height = instance.texture_size[1] + 20

                lbl.bind(width=update_label)
                lbl.width = self.spot_list.width  # trigger width assignment
                self.spot_list.add_widget(lbl)

        except Exception as e:
            self.spot_list.add_widget(Label(text="Error loading safe spots.", size_hint_y=None, height=40))
            print("Error loading saved_spots.json:", e)