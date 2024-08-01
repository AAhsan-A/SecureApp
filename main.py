# main.py

import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

class MyApp(App):

    def build(self):
        # Set the background color
        Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background

        # Main layout
        main_layout = AnchorLayout(anchor_x='center', anchor_y='center')

        # Scroll view for better UX on smaller screens
        scroll_view = ScrollView(size_hint=(None, None), size=(400, 600))

        # Content layout
        content_layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(None, None), size=(400, 600))

        # Add a logo image (optional)
        logo = Image(source='logo.png', size_hint=(None, None), size=(200, 200))
        content_layout.add_widget(logo)

        # Add a welcome label
        welcome_label = Label(text='Trillium Task', font_size='24sp', size_hint=(1, 0.2), color=(0, 0, 0, 1))
        content_layout.add_widget(welcome_label)

        # Add a description label
        description_label = Label(text='Please enter your username and password ', font_size='16sp', size_hint=(1, 0.2), color=(0, 0, 0, 0.7))
        content_layout.add_widget(description_label)

        # Username input
        self.username_input = TextInput(hint_text='Username', size_hint=(1, 0.2), multiline=False)
        content_layout.add_widget(self.username_input)

        # Password input
        self.password_input = TextInput(hint_text='Password', size_hint=(1, 0.2), password=True, multiline=False)
        content_layout.add_widget(self.password_input)

        # Submit button
        self.submit_button = Button(text='Submit', size_hint=(1, 0.2), background_color=(0, 0.5, 1, 1))
        self.submit_button.bind(on_press=self.encrypt_and_store)
        content_layout.add_widget(self.submit_button)

        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)

        return main_layout

    def encrypt_and_store(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            self.show_popup('Error', 'Username and Password cannot be empty!')
            return

        key = get_random_bytes(32)  # AES-256
        iv = get_random_bytes(16)

        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        encrypted_username = base64.b64encode(cipher.encrypt(username.encode())).decode('utf-8')
        encrypted_password = base64.b64encode(cipher.encrypt(password.encode())).decode('utf-8')

        data = {
            'key': base64.b64encode(key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'username': encrypted_username,
            'password': encrypted_password
        }

        with open('encrypted_data.json', 'w') as f:
            json.dump(data, f)

        self.username_input.text = ''
        self.password_input.text = ''

        self.show_popup('Success', 'Data encrypted and stored successfully!')

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message)
        popup_button = Button(text='OK', size_hint=(1, 0.5))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.5))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    MyApp().run()
