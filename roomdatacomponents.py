from datetime import datetime, timedelta

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
'''
The room data components of the app
'''


class RoomDataComponents(FloatLayout):

    room_data = None
    current_view = None

    def __init__(self, **kwargs):
        super(RoomDataComponents, self).__init__(**kwargs)

        self.current_view = FloatLayout()

        self.add_widget(self.current_view)

    # Calls for the creation of room data components
    def show_room_data(self, room_data):
        self.room_data = self.parse_room_data(room_data)
        self.create_room_stats()

    # Creates and displays the room data component components
    def create_room_stats(self):
        self.destroy_current_view()
        self.current_view.add_widget(RoomSchedule(self.room_data))
        self.current_view.add_widget(RoomInformation(self.room_data))
        self.current_view.add_widget(RoomInformation.session_view)

    # Destroys any previous room data display
    def destroy_current_view(self):
        self.remove_widget(self.current_view)
        RoomInformation.session_view = FloatLayout()

        self.current_view = FloatLayout()
        self.add_widget(self.current_view)

    # Parses raw room data into a 2D array where the outer is each individual room, and the inner is individual fields
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

        return outer_array


'''
The room schedule grid component
'''


class RoomSchedule(FloatLayout):

    time_format = "%I:%M %p"

    grid_buttons_x = 0.27
    grid_buttons_y = 0.95
    grid_button_length = 0.1
    grid_button_height = 0.030
    grid_start_time = datetime.strptime("07:00 AM", time_format)
    grid_end_time = end_time = datetime.strptime("10:00 PM", time_format)

    def __init__(self, data, **kwargs):
        super(RoomSchedule, self).__init__(**kwargs)

        self.create_schedule_col_headers()
        self.create_schedule_row_headers()
        self.create_schedule_grid_buttons()
        self.populate_schedule_data(data)

    # Creates the column headers for the schedule grid; relevant days of the week
    def create_schedule_col_headers(self):
        col_headers = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        count = self.grid_button_length
        for day in col_headers:
            self.add_widget(
                Button(text=day, pos_hint={'x': self.grid_buttons_x + count, 'y': self.grid_buttons_y},
                       size_hint=(self.grid_button_length, self.grid_button_height))
            )
            count += self.grid_button_length

    # Creates the row headers for the schedule grid; relevant day times at a set interval
    def create_schedule_row_headers(self):
        y_offset = 0

        start_time = self.grid_start_time
        num_of_grid_boxes = self.get_num_of_intervals(self.grid_start_time, self.grid_end_time, 30)
        for time in range(num_of_grid_boxes + 1):
            self.add_widget(Button(
                text=start_time.strftime(self.time_format),
                pos_hint={'x': self.grid_buttons_x, 'y': self.grid_buttons_y - self.grid_button_height - y_offset},
                size_hint=(self.grid_button_length, self.grid_button_height)
            ))

            start_time = start_time + timedelta(minutes=30)
            y_offset += self.grid_button_height

    # Creates an empty even grid for class sessions
    def create_schedule_grid_buttons(self):
        time_grid = GridLayout(
            size_hint=(self.grid_button_length * 6, self.grid_button_height * 31),
            pos_hint={
                'x': self.grid_buttons_x + self.grid_button_length,
                'y': self.grid_buttons_y - (self.grid_button_height * 31)
            },
            cols=6, rows=31
        )

        for tile in range(time_grid.cols * time_grid.rows):
            available_button = Button()
            available_button.disabled = True
            time_grid.add_widget(available_button)

        self.add_widget(time_grid)

    # Populates the empty schedule grid with schedule data for the given room
    def populate_schedule_data(self, room_data):
        time_sub_section = self.grid_button_height / 6

        for room in room_data:
            # Splits trailing seconds (always 00), AM and PM times
            start_time = datetime.strptime(room[7][:-6] + room[7][-3:], self.time_format)
            end_time = datetime.strptime(room[8][:-6] + room[8][-3:], self.time_format)
            button_height = self.get_num_of_intervals(start_time, end_time, 5) * time_sub_section

            counter = 1
            for day in room[9:15]:
                if day == "Y":
                    y_offset = self.get_num_of_intervals(self.grid_start_time, start_time, 5) * time_sub_section

                    self.create_session_button(start_time, end_time, counter, button_height, y_offset, room)

                counter += 1

    # Creates a button for given session data; clicking populates room information view
    def create_session_button(self, start_time, end_time, counter, button_height, y_offset, room):
        session_button = Button(
            text=start_time.strftime(self.time_format) + " " + end_time.strftime(self.time_format),
            pos_hint={
                'x': self.grid_buttons_x + (counter * self.grid_button_length),
                'y': self.grid_buttons_y - button_height - y_offset
            },
            size_hint=(self.grid_button_length, button_height)
        )
        session_button.bind(on_press=lambda x: RoomInformation.create_session_information_view(room))
        self.add_widget(session_button)

    # Calculates the number of given time intervals between the given start and end time
    @staticmethod
    def get_num_of_intervals(start_time, end_time, interval_length):
        counter = 0
        while start_time < end_time:
            start_time = start_time + timedelta(minutes=interval_length)
            counter += 1

        return counter


'''
The view of room and session specific information
'''


class RoomInformation(FloatLayout):

    session_view = FloatLayout()

    def __init__(self, data, **kwargs):
        super(RoomInformation, self).__init__(**kwargs)

        self.create_room_information_view(data)

    # Populates RoomInformation with the given room data
    def create_room_information_view(self, data):

        bldg_name = Button(text="BUILDING: " + data[0][6][:-4], size_hint=(0.2, 0.04), pos_hint={'x': 0.025, 'y': 0.58})
        bldg_name.background_color = (0, 0.2, 1, 1)

        room_num = Button(text="ROOM: " + data[0][6][-4:], size_hint=(0.2, 0.04), pos_hint={'x': 0.025, 'y': 0.54})
        room_num.background_color = (0, 0.2, 1, 1)

        departments = set()

        for session in data:
            departments.add(session[0])

        department_display = Button(
            text="DEPARTMENTS: " + "".join([str(x) + " & " for x in list(departments)])[:-3],
            size_hint=(0.2, 0.04), pos_hint={'x': 0.025, 'y': 0.50}
        )
        department_display.background_color = (0, 0.2, 1, 1)

        session_break = Button(text="SESSION INFORMATION", size_hint=(0.2, 0.04), pos_hint={'x': 0.025, 'y': 0.46})
        session_break.background_color = (0, 1, 0.2, 1)

        self.add_widget(bldg_name)
        self.add_widget(room_num)
        self.add_widget(department_display)
        self.add_widget(session_break)

    # Populates the given session specific data when that session data button was pressed
    @staticmethod
    def create_session_information_view(data):
        RoomInformation.session_view.clear_widgets()

        session_dept = Button(
            text="SESSION'S DEPARTMENT: " + data[0], size_hint=(0.2, 0.04), pos_hint={'x': 0.025, 'y': 0.42}
        )
        session_dept.background_color = (0, 1, 0.2, 1)

        session_name = Button(text="CLASS NAME: " + data[2], size_hint=(0.2, 0.04), pos_hint={'x': 0.025, 'y': 0.38})
        session_name.background_color = (0, 1, 0.2, 1)

        instructor_name = Button(
            text="INSTRUCTOR NAME: " + data[15], size_hint=(0.2, 0.04), pos_hint={'x': 0.025, 'y': 0.34}
        )
        instructor_name.background_color = (0, 1, 0.2, 1)

        instructor_eid = Button(
            text="INSTRUCTOR EID: " + data[16], size_hint=(0.2, 0.04), pos_hint={'x': 0.025, 'y': 0.30}
        )
        instructor_eid.background_color = (0, 1, 0.2, 1)

        RoomInformation.session_view.add_widget(session_dept)
        RoomInformation.session_view.add_widget(session_name)
        RoomInformation.session_view.add_widget(instructor_name)
        RoomInformation.session_view.add_widget(instructor_eid)
