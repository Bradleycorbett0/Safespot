import webbrowser
import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

FIREBASE_URL = "https://safespot-c5e02-default-rtdb.europe-west1.firebasedatabase.app"


class EventsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Scrollable list
        self.scrollview = ScrollView(size_hint=(1, 0.75))
        self.content = GridLayout(cols=1, size_hint_y=None, spacing=20, padding=[10, 10])
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scrollview.add_widget(self.content)
        self.layout.add_widget(self.scrollview)

        # Button row (Add + Maps)
        button_bar = BoxLayout(size_hint=(1, 0.1), spacing=10)
        add_btn = Button(text='Add', background_color=(0.1, 0.3, 0.2, 1))
        maps_btn = Button(text='Open Google Maps', background_color=(0.2, 0.4, 0.6, 1))
        add_btn.bind(on_press=self.open_add_popup)
        maps_btn.bind(on_press=self.open_google_maps)
        button_bar.add_widget(add_btn)
        button_bar.add_widget(maps_btn)
        self.layout.add_widget(button_bar)

        # Back button
        back_btn = Button(
            text='Back to Home',
            size_hint=(1, 0.1),
            background_color=(0.2, 0.1, 0.05, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self, *args):
        self.refresh_events()

    # --- Firebase functions ---
    def fetch_events_from_firebase(self):
        try:
            response = requests.get(f"{FIREBASE_URL}/events.json")
            if response.ok and response.json():
                data = response.json()
                return [{"id": k, "text": v["text"]} for k, v in data.items() if isinstance(v, dict)]
            return []
        except Exception as e:
            print("Error fetching events:", e)
            return []

    def add_event_to_firebase(self, text):
        try:
            data = {"text": text}
            response = requests.post(f"{FIREBASE_URL}/events.json", json=data)
            return response.ok
        except Exception as e:
            print("Error adding event:", e)
            return False

    def delete_event_from_firebase(self, event_id):
        try:
            response = requests.delete(f"{FIREBASE_URL}/events/{event_id}.json")
            return response.ok
        except Exception as e:
            print("Error deleting event:", e)
            return False

    def refresh_events(self):
        self.content.clear_widgets()
        events = self.fetch_events_from_firebase()

        if not events:
            self.content.add_widget(Label(
                text="No events yet.",
                font_size='20sp',
                color=(0.2, 0.2, 0.2, 1),
                size_hint_y=None,
                height=50
            ))
            return

        for event in events:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)

            lbl = Label(
                text=event['text'],
                font_size='18sp',
                color=(0.1, 0.1, 0.1, 1),
                halign='left',
                valign='middle'
            )
            lbl.bind(width=lambda inst, val: setattr(inst, 'text_size', (val - 40, None)))
            lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', max(val[1] + 10, 80)))

            delete_btn = Button(
                text="Delete",
                size_hint=(None, 1),
                width=100,
                background_color=(0.8, 0.3, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            delete_btn.bind(on_release=lambda btn, i=event["id"]: self.delete_and_refresh(i))

            row.add_widget(lbl)
            row.add_widget(delete_btn)
            self.content.add_widget(row)

    def delete_and_refresh(self, event_id):
        if self.delete_event_from_firebase(event_id):
            self.refresh_events()
        else:
            self.show_popup("Error", "Failed to delete event.")

    # --- Add event popup ---
    def open_add_popup(self, instance):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_field = TextInput(
            hint_text='Enter new event details (or location name)',
            multiline=True,
            size_hint_y=0.7,
            font_size='18sp'
        )
        box.add_widget(input_field)

        def save_event(_):
            new_event = input_field.text.strip()
            if new_event:
                if self.add_event_to_firebase(new_event):
                    self.refresh_events()
                else:
                    self.show_popup("Error", "Failed to save event.")
            popup.dismiss()

        save_btn = Button(text="Save", background_color=(0.1, 0.4, 0.2, 1))
        save_btn.bind(on_press=save_event)
        box.add_widget(save_btn)

        popup = Popup(title="Add Event", content=box, size_hint=(0.9, 0.5))
        popup.open()

    # --- Google Maps ---
    def open_google_maps(self, instance):
        """
        Opens Google Maps. If you later store lat/lon or location name,
        you can change this to open directions to a specific spot.
        """
        try:
            webbrowser.open("https://www.google.com/maps")
        except Exception as e:
            self.show_popup("Error", f"Could not open Maps: {e}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()