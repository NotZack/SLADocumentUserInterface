from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

import rootlayout
import socketcomm


class SearchComponents(FloatLayout):

    def __init__(self, **kwargs):
        super(SearchComponents, self).__init__(**kwargs)
        self.search_input = TextInput(multiline=False, size_hint=(0.10, 0.05), pos_hint={'x': 0.025, 'y': 0.90})
        self.search_input.bind(text=self.on_type)

        self.search_button = Button(text='Search', size_hint=(0.10, 0.05), pos_hint={'x': 0.125, 'y': 0.90})
        self.search_button.bind(on_press=self.on_search_press)

        self.search_results = GridLayout(cols=1, size_hint=(0.2, 0.25), pos_hint={'x': 0.025, 'y': 0.65})

        self.add_widget(self.search_button)
        self.add_widget(self.search_input)
        self.add_widget(self.search_results)

    def on_search_press(self, button):
        socketcomm.send_query_to_socket(self.search_input.text)

    def on_type(self, instance, text):
        self.search_results.clear_widgets()

        query_result = socketcomm.send_query_to_socket(self.search_input.text)
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
        room_data = socketcomm.collect_room_data(button.text)

        rootlayout.root.room_data_display.show_room_data(room_data)

