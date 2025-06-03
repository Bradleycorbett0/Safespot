from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
import json
import os


class CommentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        self.scrollview = ScrollView(size_hint=(1, 0.8))
        self.content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scrollview.add_widget(self.content)
        layout.add_widget(self.scrollview)

        # Add Comment button
        btn_add = Button(
            text="Add Comment",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.4, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        btn_add.bind(on_release=self.open_add_comment_popup)
        layout.add_widget(btn_add)

        # Back button
        btn_back = Button(
            text="Back to Home",
            size_hint=(1, 0.1),
            background_color=(0.4, 0.25, 0.15, 1),
            color=(1, 1, 1, 1)
        )
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)

        self.add_widget(layout)
        self.load_comments()

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def load_comments(self):
        self.content.clear_widgets()
        comments_file = "comments.json"

        if os.path.exists(comments_file):
            try:
                with open(comments_file, "r") as file:
                    comments_data = json.load(file)

                if not comments_data:
                    self.content.add_widget(Label(text="No comments available.", size_hint_y=None, height=40))
                    return

                for comment in sorted(comments_data, key=lambda x: x.get('spot_name', '').lower()):
                    lbl = Label(
                        text=f"[b]{comment['spot_name']}[/b]: {comment['comment']}",
                        markup=True,
                        size_hint_y=None,
                        height=40,
                        color=(0, 0, 0, 1)
                    )
                    lbl.bind(on_touch_down=lambda instance, touch, c=comment: self.show_comment_popup(c) if instance.collide_point(*touch.pos) else None)
                    self.content.add_widget(lbl)
            except Exception as e:
                self.content.add_widget(Label(text="Error loading comments.", size_hint_y=None, height=40))
                print("Comment loading error:", e)
        else:
            self.content.add_widget(Label(text="No comments file found.", size_hint_y=None, height=40))

    def open_add_comment_popup(self, instance):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        spot_input = TextInput(hint_text="Spot Name", multiline=False)
        comment_input = TextInput(hint_text="Comment", multiline=True)

        save_btn = Button(text="Save", size_hint=(1, None), height=40)
        cancel_btn = Button(text="Cancel", size_hint=(1, None), height=40)

        box.add_widget(spot_input)
        box.add_widget(comment_input)
        box.add_widget(save_btn)
        box.add_widget(cancel_btn)

        popup = Popup(title="Add Comment", content=box, size_hint=(0.9, 0.7))

        def save_comment(instance):
            name = spot_input.text.strip()
            comment = comment_input.text.strip()
            if name and comment:
                self.save_comment(name, comment)
                popup.dismiss()
                self.load_comments()

        save_btn.bind(on_release=save_comment)
        cancel_btn.bind(on_release=popup.dismiss)
        popup.open()

    def save_comment(self, spot_name, comment):
        comments_file = "comments.json"
        comments = []
        if os.path.exists(comments_file):
            with open(comments_file, "r") as file:
                try:
                    comments = json.load(file)
                except:
                    comments = []

        comments.append({"spot_name": spot_name, "comment": comment})

        with open(comments_file, "w") as file:
            json.dump(comments, file, indent=2)

    def show_comment_popup(self, comment_data):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text=f"{comment_data['spot_name']}: {comment_data['comment']}", size_hint_y=None))

        delete_btn = Button(text="Delete Comment", size_hint=(1, None), height=40, background_color=(0.6, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        close_btn = Button(text="Close", size_hint=(1, None), height=40)

        box.add_widget(delete_btn)
        box.add_widget(close_btn)

        popup = Popup(title="Comment Options", content=box, size_hint=(0.85, 0.5))

        def delete_and_close(instance):
            self.delete_comment(comment_data)
            popup.dismiss()
            self.load_comments()

        delete_btn.bind(on_release=delete_and_close)
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def delete_comment(self, target_comment):
        comments_file = "comments.json"
        if os.path.exists(comments_file):
            with open(comments_file, "r") as file:
                comments = json.load(file)

            updated_comments = [c for c in comments if not (c["spot_name"] == target_comment["spot_name"] and c["comment"] == target_comment["comment"])]

            with open(comments_file, "w") as file:
                json.dump(updated_comments, file, indent=2)