from kivy.uix.floatlayout import FloatLayout

import roomdatacomponents
import searchcomponents


class RootLayout(FloatLayout):

    search_display = None
    room_data_display = None

    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)

        self.search_display = searchcomponents.SearchComponents()
        self.room_data_display = roomdatacomponents.RoomDataComponents()

        self.add_widget(self.search_display)
        self.add_widget(self.room_data_display)


root = RootLayout()
