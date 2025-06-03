import os import shutil from kivy.uix.screenmanager import Screen from kivy.uix.boxlayout import BoxLayout from kivy.uix.button import Button from kivy.uix.label import Label from kivy.uix.image import Image from kivy.graphics import Color, Rectangle from plyer import filechooser

class UploadPhotoScreen(Screen): def init(self, **kwargs): super().init(**kwargs)

with self.canvas.before:
        Color(1, 0.98, 0.94, 1)
        self.bg_rect = Rectangle(pos=self.pos, size=self.size)
    self.bind(size=self._update_bg, pos=self._update_bg)

    self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
    self.add_widget(self.layout)

    self.label = Label(text="Select a picture to upload", font_size='18sp')
    self.layout.add_widget(self.label)

    self.img = Image(source='', size_hint=(1, 0.6), allow_stretch=True)
    self.layout.add_widget(self.img)

    self.select_btn = Button(text="Choose Image", background_color=(0.4, 0.6, 0.8, 1))
    self.select_btn.bind(on_release=self.choose_file)
    self.layout.add_widget(self.select_btn)

    self.back_btn = Button(text="Back to Home", background_color=(0.6, 0.4, 0.4, 1))
    self.back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
    self.layout.add_widget(self.back_btn)

def _update_bg(self, *args):
    self.bg_rect.pos = self.pos
    self.bg_rect.size = self.size

def choose_file(self, *args):
    filechooser.open_file(on_selection=self.handle_selection)

def handle_selection(self, selection):
    if selection:
        source = selection[0]
        self.img.source = source
        self.img.reload()

        target_folder = "/storage/emulated/0/safespot/photos"
        os.makedirs(target_folder, exist_ok=True)
        filename = os.path.basename(source)
        shutil.copy(source, os.path.join(target_folder, filename))

        self.label.text = f"Image saved: {filename}"

