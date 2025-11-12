from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView

Window.clearcolor = (1, 0.97, 0.93, 1)  # Soft warm tone

class AdPermissionScreen(Screen):
    def on_enter(self):
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))

        # Add logo or ad icon if available
        layout.add_widget(Image(source='assets/ad_icon.png', size_hint=(1, 0.25)))

        # Add explanatory text
        layout.add_widget(Label(
            text="We use occasional ads to keep SafeSpot 100% free.\n\nWould you like to allow relevant adverts?",
            font_size='17sp',
            halign='center',
            valign='middle',
            color=(0.2, 0.2, 0.2, 1),
        ))

        layout.add_widget(Widget(size_hint_y=None, height=dp(10)))  # Spacer

        # Buttons row
        button_row = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(20))
        
        btn_allow = Button(
            text="Allow Ads",
            background_color=(0.2, 0.5, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        btn_deny = Button(
            text="No Thanks",
            background_color=(0.6, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='16sp'
        )

        btn_allow.bind(on_release=self.allow_ads)
        btn_deny.bind(on_release=self.deny_ads)

        button_row.add_widget(btn_allow)
        button_row.add_widget(btn_deny)
        layout.add_widget(button_row)

        self.add_widget(layout)

    def allow_ads(self, instance):
        App.get_running_app().save_user_data('ad_consent', True)
        self.manager.current = 'home'

    def deny_ads(self, instance):
        App.get_running_app().save_user_data('ad_consent', False)
        self.manager.current = 'home'