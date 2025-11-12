from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import requests
import webbrowser

# ✅ Firebase base path
BASE_URL = "https://safespot-c5e02-default-rtdb.europe-west1.firebasedatabase.app/spots"


class SpotsScreen(Screen):
    def on_pre_enter(self):
        """Called every time the screen is entered"""
        self.load_cities()

    def load_cities(self):
        """Loads all available cities from Firebase"""
        self.clear_widgets()
        scroll = ScrollView(size_hint=(1, 1))
        container = BoxLayout(orientation="vertical", size_hint_y=None, padding=20, spacing=10)
        container.bind(minimum_height=container.setter("height"))

        try:
            response = requests.get(f"{BASE_URL}.json")
            if response.status_code == 200:
                data = response.json()
                if data:
                    for city_name in sorted(data.keys()):
                        btn = Button(
                            text=city_name.title().replace("_", " "),
                            size_hint_y=None,
                            height=60,
                            background_color=(0.15, 0.15, 0.15, 1),
                            color=(1, 1, 1, 1),
                            on_press=lambda instance, city=city_name: self.show_spots(city)
                        )
                        container.add_widget(btn)
                else:
                    container.add_widget(Label(
                        text="No data available.",
                        size_hint_y=None,
                        height=60,
                        color=(0, 0, 0, 1)
                    ))
            else:
                container.add_widget(Label(
                    text="Error fetching data from Firebase.",
                    size_hint_y=None,
                    height=60,
                    color=(0, 0, 0, 1)
                ))
        except Exception as e:
            container.add_widget(Label(
                text=f"Error: {e}",
                size_hint_y=None,
                height=60,
                color=(0, 0, 0, 1)
            ))

        # ✅ Add Back to Home button at the bottom
        back_btn = Button(
            text="← Back to Home",
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_press=lambda x: self.go_home())
        container.add_widget(back_btn)

        scroll.add_widget(container)
        self.add_widget(scroll)

    def go_home(self):
        """Return to home screen"""
        self.manager.current = "home"

    def show_spots(self, city):
        """Show all safe spots for the selected city"""
        self.clear_widgets()
        scroll = ScrollView(size_hint=(1, 1))
        container = BoxLayout(orientation="vertical", size_hint_y=None, padding=20, spacing=15)
        container.bind(minimum_height=container.setter("height"))

        try:
            url = f"{BASE_URL}/{city}.json"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    for spot_id, spot_info in data.items():
                        name = spot_info.get("name", "Unknown")
                        desc = spot_info.get("description", "No description available")
                        location = spot_info.get("location", name)

                        # Each spot box
                        info_box = BoxLayout(orientation="vertical", size_hint_y=None, height=190, spacing=8)
                        lbl = Label(
                            text=f"[b]{name}[/b]\n{desc}",
                            markup=True,
                            halign="left",
                            valign="middle",
                            size_hint_y=None,
                            height=90,
                            color=(0, 0, 0, 1)
                        )
                        lbl.text_size = (700, None)

                        # Buttons row
                        btn_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=10)

                        directions_btn = Button(
                            text="📍 Get Directions",
                            size_hint_x=0.5,
                            background_color=(0.1, 0.5, 0.1, 1),
                            color=(1, 1, 1, 1),
                            on_press=lambda x, loc=location: self.open_directions(loc)
                        )

                        delete_btn = Button(
                            text="🗑 Delete",
                            size_hint_x=0.5,
                            background_color=(0.6, 0, 0, 1),
                            color=(1, 1, 1, 1),
                            on_press=lambda x, cid=city, sid=spot_id, sname=name: self.confirm_delete(cid, sid, sname)
                        )

                        btn_row.add_widget(directions_btn)
                        btn_row.add_widget(delete_btn)

                        info_box.add_widget(lbl)
                        info_box.add_widget(btn_row)
                        container.add_widget(info_box)
                else:
                    container.add_widget(Label(
                        text="No safe spots found for this city.",
                        size_hint_y=None,
                        height=60,
                        color=(0, 0, 0, 1)
                    ))
            else:
                container.add_widget(Label(
                    text="Error fetching city data.",
                    size_hint_y=None,
                    height=60,
                    color=(0, 0, 0, 1)
                ))
        except Exception as e:
            container.add_widget(Label(
                text=f"Error: {e}",
                size_hint_y=None,
                height=60,
                color=(0, 0, 0, 1)
            ))

        back_btn = Button(
            text="← Back to Cities",
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            on_press=lambda x: self.load_cities()
        )
        container.add_widget(back_btn)

        scroll.add_widget(container)
        self.add_widget(scroll)

    def open_directions(self, location):
        """Open Google Maps for the given location"""
        maps_url = f"https://www.google.com/maps/search/?api=1&query={location.replace(' ', '+')}"
        webbrowser.open(maps_url)

    def confirm_delete(self, city, spot_id, name):
        """Show confirmation popup before deleting"""
        box = BoxLayout(orientation="vertical", padding=15, spacing=10)
        msg = Label(text=f"Are you sure you want to delete:\n[b]{name}[/b]?", markup=True, color=(0, 0, 0, 1))
        btn_row = BoxLayout(spacing=10, size_hint_y=None, height=50)

        yes_btn = Button(text="Yes, Delete", background_color=(0.7, 0, 0, 1), color=(1, 1, 1, 1))
        no_btn = Button(text="Cancel", background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1))

        popup = Popup(title="Confirm Delete", content=box, size_hint=(0.8, 0.4))
        yes_btn.bind(on_press=lambda x: (self.delete_spot(city, spot_id), popup.dismiss()))
        no_btn.bind(on_press=lambda x: popup.dismiss())

        btn_row.add_widget(yes_btn)
        btn_row.add_widget(no_btn)
        box.add_widget(msg)
        box.add_widget(btn_row)
        popup.open()

    def delete_spot(self, city, spot_id):
        """Delete a safe spot from Firebase"""
        try:
            url = f"{BASE_URL}/{city}/{spot_id}.json"
            response = requests.delete(url)
            if response.status_code == 200:
                print(f"Deleted {spot_id} from {city}")
                self.show_spots(city)
            else:
                print("Error deleting spot:", response.text)
        except Exception as e:
            print("Error deleting spot:", e)