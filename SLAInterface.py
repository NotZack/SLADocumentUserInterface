import socket
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

kivy.require('1.11.0')

client_socket = socket.socket()


def open_socket(port_number):
    host = socket.gethostname()
    port = port_number
    client_socket.connect((host, port))


def send_to_socket(message):
    client_socket.sendall((message + '\n').encode())
    data = client_socket.recv(1024).decode()
    print('Received from server: ' + data)


class SearchBar(GridLayout):

    def __init__(self, **kwargs):
        super(SearchBar, self).__init__(**kwargs)
        self.cols = 2

        search_button = Button(text='Search')
        search_button.bind(on_press=self.search_btn_pressed)

        self.searchInput = TextInput(multiline=False)
        self.add_widget(search_button)
        self.add_widget(self.searchInput)

    def search_btn_pressed(self, button):
        send_to_socket(self.searchInput.text)


class InterfaceGUIApplication(App):
    def build(self):
        return SearchBar()


if __name__ == '__main__':
    open_socket(5119)
    InterfaceGUIApplication().run()
