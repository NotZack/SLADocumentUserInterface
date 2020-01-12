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
            self.current_view = RoomSchedule(self.room_data)
            self.add_widget(self.current_view)

        else:
            self.daily_toggle.disabled = False
            self.information_toggle.disabled = True

            self.destroy_current_view()
            self.current_view = RoomInformation(self.room_data)
            self.add_widget(self.current_view)

    def show_room_data(self, room_data):
        self.room_data = self.parse_room_data(room_data)
        self.check_toggle_state(None)

    # TODO
    def destroy_current_view(self):
        self.remove_widget(self.current_view)
        self.current_view = None

    @staticmethod
    def parse_room_data(raw_data):
        raw_data = raw_data[1:-1]
        raw_data = raw_data.replace(", [", "").replace("[", "")

        outer_array = []
        for room in raw_data.split(']'):
            inner_array = []

            for field in room.split(','):
                inner_array.append(field.strip())

            if len(inner_array) > 1 and (len(outer_array) == 0 or (outer_array[len(outer_array) - 1] != inner_array)):
                outer_array.append(inner_array)

        for x in outer_array:
            print(x, " ")

        return outer_array


class RoomSchedule(FloatLayout):

    # available_button.background_normal = ""
    # available_button.background_color = (1, 0, 0, 1)

    time_format = "%I:%M %p"

    grid_button_length = 0.09
    grid_button_height = 0.024
    grid_start_time = datetime.strptime("07:00 AM", time_format)
    grid_end_time = end_time = datetime.strptime("10:00 PM", time_format)

    def __init__(self, data, **kwargs):
        super(RoomSchedule, self).__init__(**kwargs)

        self.create_schedule_col_headers()
        self.create_schedule_row_headers()
        self.create_schedule_grid_buttons()
        self.populate_schedule_data(data)

    def create_schedule_col_headers(self):
        col_headers = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        count = self.grid_button_length
        for day in col_headers:
            self.add_widget(
                Button(text=day, pos_hint={'x': 0.32 + count, 'y': 0.8}, size_hint=(self.grid_button_length, 0.032))
            )
            count += self.grid_button_length

    def create_schedule_row_headers(self):
        count = self.grid_button_height

        start_time = self.grid_start_time
        for time in range(self.get_num_of_intervals(self.grid_start_time, self.grid_end_time, 30) + 1):
            self.add_widget(Button(
                text=start_time.strftime(self.time_format),
                pos_hint={'x': 0.32, 'y': 0.8 - count},
                size_hint=(self.grid_button_length, self.grid_button_height)
            ))

            start_time = start_time + timedelta(minutes=30)
            count += self.grid_button_height

    def create_schedule_grid_buttons(self):
        time_grid = GridLayout(
            size_hint=(self.grid_button_length * 6, self.grid_button_height * 31),
            pos_hint={'x': 0.41, 'y': 0.056},
            cols=6, rows=31
        )

        for tile in range(time_grid.cols * time_grid.rows):
            available_button = Button()
            available_button.disabled = True
            time_grid.add_widget(available_button)

        self.add_widget(time_grid)

    def populate_schedule_data(self, room_data):
        time_sub_section = self.grid_button_height / 6

        for room in room_data:
            start_time = datetime.strptime(room[7][:-6] + room[7][-3:], self.time_format)
            end_time = datetime.strptime(room[8][:-6] + room[7][-3:], self.time_format)
            button_height = self.get_num_of_intervals(start_time, end_time, 5) * time_sub_section

            counter = 1
            for day in room[9:15]:
                if day == "Y":
                    y_offset = self.get_num_of_intervals(self.grid_start_time, start_time, 5) * time_sub_section

                    self.add_widget(
                        Button(
                            text=start_time.strftime(self.time_format) + " " + end_time.strftime(self.time_format),
                            pos_hint={
                                'x': 0.32 + (counter * self.grid_button_length),
                                'y': (0.8 - button_height) - y_offset
                            },
                            size_hint=(0.09, button_height)
                        )
                    )
                counter += 1

    @staticmethod
    def get_num_of_intervals(start_time, end_time, interval_length):
        counter = 0
        while start_time < end_time:
            start_time = start_time + timedelta(minutes=interval_length)
            counter += 1

        return counter


class RoomInformation(FloatLayout):

    def __init__(self, data, **kwargs):
        super(RoomInformation, self).__init__(**kwargs)
