import kivy
from kivy import Config
from kivy.app import App

import rootlayout
import socketcomm

Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1020')
kivy.require('1.11.0')


class InterfaceGUIApplication(App):
    def build(self):
        return rootlayout.root


if __name__ == '__main__':
    socketcomm.open_socket(5119)
    InterfaceGUIApplication().run()
