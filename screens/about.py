import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # --- Background ---
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # --- Main layout ---
        layout = BoxLayout(orientation='vertical', padding=[30, 35, 30, 15], spacing=8)

        # --- Larger logo ---
        logo_path = "/storage/emulated/0/safespot/logo.png"
        if os.path.exists(logo_path):
            logo = Image(
                source=logo_path,
                size_hint=(1, 1.2),
                allow_stretch=True,
                keep_ratio=True
            )
            layout.add_widget(logo)

        # --- Tagline ---
        tagline = Label(
            text="[b]Built from my own struggle.[/b]",
            markup=True,
            font_size='18sp',
            halign='center',
            valign='middle',
            color=(0.15, 0.1, 0.05, 1)
        )
        tagline.bind(size=tagline.setter('text_size'))
        layout.add_widget(tagline)

        # --- Story text ---
        story_text = (
            "I’ve been homeless. Missed last trains. Slept cold.\n\n"
            "But I used those moments — on city benches, in dark corners — "
            "to write my books, build my games, and dream up SafeSpot.\n\n"
            "It’s more than an app.\n"
            "It’s a map of quiet places, trusted locations, and emergency help — "
            "for anyone who’s ever needed safety on the go."
        )
        story = Label(
            text=story_text,
            font_size='15sp',
            halign='center',
            valign='top',
            color=(0.1, 0.1, 0.1, 1)
        )
        story.bind(size=story.setter('text_size'))
        layout.add_widget(story)

        # --- Divider ---
        divider = Label(text="— — —", font_size='18sp', halign='center', color=(0.25, 0.2, 0.15, 1))
        divider.bind(size=divider.setter('text_size'))
        layout.add_widget(divider)

        # --- Features with icons (DOUBLE SIZE) ---
        icons_path = "/storage/emulated/0/safespot/icons/"
        features_data = [
            (os.path.join(icons_path, "save_icon.png"), "Save safe spots"),
            (os.path.join(icons_path, "comment_icon.png"), "Add real comments"),
            (os.path.join(icons_path, "emergency_icon.png"), "Emergency contacts ready"),
            (os.path.join(icons_path, "mind_icon.png"), "Calm design. Real impact."),
        ]

        features_box = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None)
        features_box.bind(minimum_height=features_box.setter('height'))

        for icon_path, text in features_data:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=90, spacing=18)
            if os.path.exists(icon_path):
                icon = Image(source=icon_path, size_hint=(None, 1), width=90, allow_stretch=True, keep_ratio=True)
            else:
                icon = Label(text="•", font_size='32sp', color=(0.1, 0.1, 0.1, 1), size_hint=(None, 1), width=40)

            lbl = Label(
                text=text,
                font_size='28sp',   # doubled from 15sp → 28sp
                halign='left',
                valign='middle',
                color=(0.1, 0.1, 0.1, 1)
            )
            lbl.bind(size=lbl.setter('text_size'))
            row.add_widget(icon)
            row.add_widget(lbl)
            features_box.add_widget(row)

        layout.add_widget(features_box)

        # --- Buttons ---
        privacy_btn = Button(
            text='View Privacy Policy',
            size_hint=(1, 0.12),
            background_color=(0.35, 0.25, 0.15, 1),
            color=(1, 1, 1, 1),
            font_size='15sp'
        )
        privacy_btn.bind(on_release=self.show_privacy_policy)
        layout.add_widget(privacy_btn)

        back_btn = Button(
            text='Back to Home',
            size_hint=(1, 0.12),
            background_color=(0.25, 0.15, 0.1, 1),
            color=(1, 1, 1, 1),
            font_size='15sp'
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    # --- Privacy Policy popup ---
    def show_privacy_policy(self, instance):
        content = (
            "[b]Privacy Policy[/b]\n\n"
            "SafeSpot respects your privacy and your trust means everything to us.\n\n"
            "• Your data is securely stored in Google Firebase.\n"
            "• No personal information is shared with third parties.\n"
            "• Location data is used only to show nearby safe spots.\n"
            "• You can delete your data at any time.\n\n"
            "SafeSpot was created to protect — not to collect."
        )

        label = Label(
            text=content,
            markup=True,
            font_size='15sp',
            halign='left',
            valign='top',
            color=(0.1, 0.1, 0.1, 1)
        )
        label.bind(size=label.setter('text_size'))

        close_btn = Button(
            text="Close",
            size_hint=(1, 0.18),
            background_color=(0.35, 0.25, 0.15, 1),
            color=(1, 1, 1, 1),
            font_size='15sp'
        )

        box = BoxLayout(orientation='vertical', padding=20, spacing=15)
        box.add_widget(label)
        box.add_widget(close_btn)

        popup = Popup(
            title="Privacy Policy",
            content=box,
            size_hint=(0.9, 0.75),
            background_color=(1, 0.98, 0.94, 1),
            title_color=(0.15, 0.1, 0.05, 1),
            separator_color=(0.35, 0.25, 0.15, 1)
        )

        close_btn.bind(on_release=popup.dismiss)
        popup.open()