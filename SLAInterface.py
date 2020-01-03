import socket
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config

Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1020')
kivy.require('1.11.0')

client_socket = socket.socket()


def open_socket(port_number):
    host = socket.gethostname()
    port = port_number
    client_socket.connect((host, port))


def send_to_socket(message):
    client_socket.sendall((message + '\n').encode())
    data = client_socket.recv(1024).decode()
    print(data)
    return data


class SearchBar(FloatLayout):

    def __init__(self, **kwargs):
        super(SearchBar, self).__init__(**kwargs)

        self.search_input = TextInput(multiline=False, size_hint=(0.10, 0.033), pos_hint={'x': 0.05, 'y': 0.90})
        self.search_input.bind(text=self.on_type)

        self.search_button = Button(text='Search', size_hint=(0.10, 0.033), pos_hint={'x': 0.15, 'y': 0.90})
        self.search_button.bind(on_press=self.send_exact_search)

        self.search_results = GridLayout(cols=1, size_hint=(0.2, 0.25), pos_hint={'x': 0.05, 'y': 0.65})

        self.add_widget(self.search_button)
        self.add_widget(self.search_input)
        self.add_widget(self.search_results)

    def send_exact_search(self, button):
        print("Search button pressed")
        send_to_socket(self.search_input.text)

    def on_type(self, instance, text):
        self.search_results.clear_widgets()

        for data in send_to_socket(self.search_input.text).split(','):
            if len(data) > 2:
                # , background_normal='', background_color=(0,0,0,0)
                result_button = Button(text=data, size_hint=(0.1, 0.03))
                result_button.bind(on_press=self.update_textfield_text)
                self.search_results.add_widget(result_button)

    def update_textfield_text(self, button):
        self.search_input.text = button.text
        self.send_exact_search(None)


class InterfaceGUIApplication(App):
    def build(self):
        return SearchBar()


if __name__ == '__main__':
    open_socket(5119)
    InterfaceGUIApplication().run()
