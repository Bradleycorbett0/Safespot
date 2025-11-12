import os
import json
import shutil
import time

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import Color, Rectangle

try:
    from android.permissions import request_permissions, Permission
    from plyer import camera
    CAMERA_AVAILABLE = True
except Exception:
    CAMERA_AVAILABLE = False

# --- Gallery storage path ---
GALLERY_PATH = "/storage/emulated/0/safespot/gallery"
SPOTS_FILE = "saved_spots.json"


class ImageGalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

        # --- Search bar ---
        self.search_input = TextInput(
            hint_text="Search by spot name...",
            multiline=False,
            size_hint_y=None,
            height=80,
            font_size='18sp',
            padding=[10, 10],
            foreground_color=(0, 0, 0, 1),
            background_color=(1, 1, 1, 1)
        )
        self.search_input.bind(text=self.update_filter)
        self.layout.add_widget(self.search_input)

        # --- ScrollView for images ---
        self.scroll = ScrollView(size_hint=(1, 1))
        self.grid = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)

        # --- Buttons ---
        button_row = BoxLayout(size_hint_y=None, height=50, spacing=10)

        upload_btn = Button(
            text="Upload",
            background_color=(0.3, 0.5, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        upload_btn.bind(on_release=self.open_file_chooser)

        camera_btn = Button(
            text="Take Photo",
            background_color=(0.4, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        camera_btn.bind(on_release=self.take_photo)

        button_row.add_widget(upload_btn)
        button_row.add_widget(camera_btn)
        self.layout.add_widget(button_row)

        # --- Back button ---
        back_btn = Button(
            text="Back to Home",
            size_hint_y=None,
            height=50,
            background_color=(0.4, 0.3, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

        if not os.path.exists(GALLERY_PATH):
            os.makedirs(GALLERY_PATH)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self):
        self.load_images()

    # ------------------ IMAGE DISPLAY ------------------
    def load_images(self, filter_text=""):
        self.grid.clear_widgets()

        if not os.path.exists(SPOTS_FILE):
            self.grid.add_widget(Label(text="No saved spots found."))
            return

        try:
            with open(SPOTS_FILE, "r") as f:
                data = json.load(f)
        except Exception as e:
            self.grid.add_widget(Label(text=f"Error reading spots: {e}"))
            return

        sorted_spots = sorted(data, key=lambda x: x["name"].lower())

        for spot in sorted_spots:
            if filter_text.lower() not in spot["name"].lower():
                continue

            spot_name = spot.get("name", "Unnamed Spot")
            image_filename = f"{spot_name.lower().replace(' ', '_')}.jpg"
            image_path = os.path.join(GALLERY_PATH, image_filename)

            if not os.path.exists(image_path):
                image_path = "placeholder.png"

            image = Image(
                source=image_path,
                size_hint_y=None,
                height=200,
                allow_stretch=True
            )
            label = Label(
                text=spot_name,
                size_hint_y=None,
                height=40,
                font_size='18sp',
                color=(0, 0, 0, 1)
            )

            self.grid.add_widget(image)
            self.grid.add_widget(label)

    def update_filter(self, instance, value):
        self.load_images(filter_text=value)

    # ------------------ FILE UPLOAD ------------------
    def open_file_chooser(self, instance):
        chooser = FileChooserIconView(path="/storage/emulated/0/", filters=["*.png", "*.jpg", "*.jpeg"])
        box = BoxLayout(orientation='vertical')
        box.add_widget(chooser)

        btn = Button(text="Select Image", size_hint_y=None, height=50)

        def save_selected(*args):
            selection = chooser.selection
            if selection:
                self.copy_image_to_gallery(selection[0])
            popup.dismiss()

        btn.bind(on_release=save_selected)
        box.add_widget(btn)

        popup = Popup(title="Choose an image", content=box, size_hint=(0.95, 0.95))
        popup.open()

    def copy_image_to_gallery(self, source_path):
        spot_name = self.search_input.text.strip()
        if not spot_name:
            self.show_popup("Error", "Please enter the spot name in the search bar first.")
            return

        filename = f"{spot_name.lower().replace(' ', '_')}.jpg"
        dest_path = os.path.join(GALLERY_PATH, filename)

        try:
            shutil.copy(source_path, dest_path)
            self.load_images(self.search_input.text)
            self.show_popup("Success", f"Image saved as {filename}")
        except Exception as e:
            self.show_popup("Error", f"Failed to upload image:\n{e}")

    # ------------------ CAMERA ------------------
    def take_photo(self, instance):
        if not CAMERA_AVAILABLE:
            self.show_popup("Camera Error", "Camera not available in this environment.")
            return

        try:
            request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        except Exception as e:
            print("Permission error:", e)

        spot_name = self.search_input.text.strip()
        if not spot_name:
            self.show_popup("Error", "Enter a spot name in the search bar first.")
            return

        filename = f"{spot_name.lower().replace(' ', '_')}_{int(time.time())}.jpg"
        dest_path = os.path.join(GALLERY_PATH, filename)

        try:
            camera.take_picture(filename=dest_path, on_complete=lambda x: self.on_camera_complete(dest_path))
        except Exception as e:
            self.show_popup("Camera Error", f"Failed to open camera:\n{e}")

    def on_camera_complete(self, path):
        if not path or not os.path.exists(path):
            self.show_popup("Error", "No photo captured.")
            return

        self.show_popup("Success", f"Saved photo:\n{os.path.basename(path)}")
        self.load_images(self.search_input.text)

    # ------------------ UTIL ------------------
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()