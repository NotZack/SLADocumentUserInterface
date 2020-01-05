import socket
import kivy
import re
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.label import Label

Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1020')
kivy.require('1.11.0')

client_socket = socket.socket()


def open_socket(port_number):
    host = socket.gethostname()
    port = port_number
    client_socket.connect((host, port))


def send_query_to_socket(message):
    client_socket.sendall((message + '\n').encode())

    data = client_socket.recv(2048).decode()
    return data


def collect_room_data(room_string):
    return send_query_to_socket("Collect_Unique_Room_Data:" + room_string)


class RootLayout(FloatLayout):

    search_display = None
    room_data_display = None

    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)

        self.search_display = SearchComponents()
        self.room_data_display = RoomDataComponents()

        self.add_widget(self.search_display)
        self.add_widget(self.room_data_display)


class SearchComponents(FloatLayout):

    def __init__(self, **kwargs):
        super(SearchComponents, self).__init__(**kwargs)
        self.search_input = TextInput(multiline=False, size_hint=(0.10, 0.033), pos_hint={'x': 0.05, 'y': 0.90})
        self.search_input.bind(text=self.on_type)

        self.search_button = Button(text='Search', size_hint=(0.10, 0.033), pos_hint={'x': 0.15, 'y': 0.90})
        self.search_button.bind(on_press=self.on_search_press)

        self.search_results = GridLayout(cols=1, size_hint=(0.2, 0.25), pos_hint={'x': 0.05, 'y': 0.65})

        self.add_widget(self.search_button)
        self.add_widget(self.search_input)
        self.add_widget(self.search_results)

    def on_search_press(self, button):
        send_query_to_socket(self.search_input.text)

    def on_type(self, instance, text):
        self.search_results.clear_widgets()

        query_result = send_query_to_socket(self.search_input.text)
        if query_result is not None:
            for data in query_result.split(','):
                if len(data) > 2:
                    # , background_normal='', background_color=(0,0,0,0)
                    result_button = Button(text=data, size_hint=(0.1, 0.03))
                    result_button.bind(on_press=self.on_room_collect)
                    self.search_results.add_widget(result_button)

    def on_room_collect(self, button):
        if ("Invalid query" in button.text) or ("No results found" in button.text):
            return

        self.search_input.text = button.text
        room_data = collect_room_data(button.text)

        root.room_data_display.show_room_data(room_data)


class RoomDataComponents(FloatLayout):

    def show_room_data(self, room_data):
        room_data = self.parse_room_data(room_data)

    @staticmethod
    def parse_room_data(raw_data):
        raw_data = raw_data[1:-1]
        raw_data = raw_data.replace(", [", "").replace("[", "")

        outer_array = []
        for room in raw_data.split(']'):
            inner_array = []

            for field in room.split(','):
                inner_array.append(field)

            if len(inner_array) > 1:
                outer_array.append(inner_array)

        for x in outer_array:
            print(*x, sep=" ")


root = RootLayout()


class InterfaceGUIApplication(App):
    def build(self):
        return root


if __name__ == '__main__':
    open_socket(5119)
    InterfaceGUIApplication().run()
