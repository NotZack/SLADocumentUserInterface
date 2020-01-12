from datetime import datetime, timedelta

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton


class RoomDataComponents(FloatLayout):

    room_data = None
    current_view = None

    def __init__(self, **kwargs):
        super(RoomDataComponents, self).__init__(**kwargs)

        self.daily_toggle = ToggleButton(
            text="Daily Schedule", state="down", group="view", size_hint=(0.1, 0.1), pos_hint={'x': 0.75, 'y': 0.90}
        )
        self.information_toggle = ToggleButton(
            text="Room Info", group="view", size_hint=(0.1, 0.1), pos_hint={'x': 0.85, 'y': 0.90}
        )

        self.daily_toggle.bind(on_release=self.check_toggle_state)
        self.information_toggle.bind(on_release=self.check_toggle_state)
        self.daily_toggle.disabled = True
        self.information_toggle.disabled = True

        self.current_view = FloatLayout()

        self.add_widget(self.daily_toggle)
        self.add_widget(self.information_toggle)
        self.add_widget(self.current_view)

    def check_toggle_state(self, button):
        if self.information_toggle.disabled:
            self.information_toggle.disabled = False
            self.daily_toggle.disabled = True

            self.destroy_current_view()
            self.current_view = RoomSchedule()
            self.add_widget(self.current_view)

        else:
            self.daily_toggle.disabled = False
            self.information_toggle.disabled = True

            self.destroy_current_view()
            self.current_view = RoomInformation()
            self.add_widget(self.current_view)

    def show_room_data(self, room_data):
        self.room_data = self.parse_room_data(room_data)
        self.check_toggle_state(None)

    # TODO
    def destroy_current_view(self):
        self.remove_widget(self.current_view)
        self.current_view = None

    @staticmethod
    def get_half_hour_intervals(start_time, end_time):
        counter = 0
        while start_time < end_time:
            start_time = start_time + timedelta(minutes=30)
            counter += 1

        return counter

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
            print(x, " ")

        return outer_array


class RoomSchedule(FloatLayout):

    def __init__(self, **kwargs):
        super(RoomSchedule, self).__init__(**kwargs)

        self.create_schedule_col_headers()
        self.create_schedule_row_headers()
        self.create_schedule_grid_buttons()
        self.populate_schedule_data()

    def create_schedule_col_headers(self):
        col_headers = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        count = 0.09
        for day in col_headers:
            self.add_widget(
                Button(text=day, pos_hint={'x': 0.32 + count, 'y': 0.8}, size_hint=(0.09, 0.032))
            )
            count += 0.09

    def create_schedule_row_headers(self):
        count = 0.024
        time_format = "%H:%M %p"
        start_time = datetime.strptime("07:00 AM", time_format)
        end_time = datetime.strptime("10:30 PM", "%I:%M %p")

        for time in range(RoomDataComponents.get_half_hour_intervals(start_time, end_time)):
            self.add_widget(Button(
                text=start_time.strftime(time_format), pos_hint={'x': 0.32, 'y': 0.8 - count}, size_hint=(0.09, 0.024)
            ))

            start_time = start_time + timedelta(minutes=30)
            count += 0.024

    def create_schedule_grid_buttons(self):
        time_grid = GridLayout(size_hint=(0.54, 0.744), pos_hint={'x': 0.41, 'y': 0.056}, cols=6, rows=31)

        for tile in range(time_grid.cols * time_grid.rows):
            available_button = Button()
            # available_button.background_normal = ""
            # available_button.background_color = (1, 0, 0, 1)
            time_grid.add_widget(available_button)

        self.add_widget(time_grid)

    def populate_schedule_data(self):
        pass


class RoomInformation(FloatLayout):

    def __init__(self, **kwargs):
        super(RoomInformation, self).__init__(**kwargs)
