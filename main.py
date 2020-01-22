from kivy.app import App

import rootlayout
import socketcomm
'''
Default kivy configuration
'''


class InterfaceGUIApplication(App):
    def build(self):
        return rootlayout.root


'''
Runs main application after opening socket
'''
if __name__ == '__main__':
    socketcomm.open_socket(5119)
    InterfaceGUIApplication().run()
