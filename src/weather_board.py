import displayio
import display_creator
from adafruit_display_text.label import Label
from config import config


class WeatherBoard:
    """
        get_new_data is a function that is expected to return a dictionarie like this:
            {
                'temp': '123'
                'main': rain,
                'description': 'thunder storms',
                'icon': 'd05'
            }
    """

    def __init__(self, get_new_data):
        self.get_new_data = get_new_data
        self.display = display_creator.create_display()
        self.parent_group = displayio.Group(max_size=5)

        self.heading_line_label = Label(config['font'], max_glyphs=10, anchor_point=(0, 0))
        self.heading_line_label.color = config['red']
        self.heading_line_label.text = config['temp']
        self.heading_line_label.x = 0

        self.heading_car_label = Label(config['font'], max_glyphs=10, anchor_point=(0, 0))
        self.heading_car_label.color = config['red']
        self.heading_car_label.text = config['main']
        self.heading_car_label.x = 14

        self.heading_dest_label = Label(config['font'], max_glyphs=10, anchor_point=(0, 0))
        self.heading_dest_label.color = config['red']
        self.heading_dest_label.text = config['description']
        self.heading_dest_label.x = 35

        self.heading_min_label = Label(config['font'], max_glyphs=10, anchor_point=(0, 0))
        self.heading_min_label.color = config['red']
        self.heading_min_label.text = config['icon']
        self.heading_min_label.x = config['matrix_width'] - (config['min_label_characters'] * config['character_width']) - 2

        self.header_group = displayio.Group(max_size=4)
        self.header_group.append(self.heading_line_label)
        self.header_group.append(self.heading_car_label)
        self.header_group.append(self.heading_dest_label)
        self.header_group.append(self.heading_min_label)

        self.parent_group.append(self.header_group)

        self.weather.append(Weather(self.parent_group))
        self.parent_group.append(self.weather)

        self.display.show(self.parent_group)

    def refresh(self) -> bool:
        print('Refreshing train information...')
        self.display.show(self.parent_group)
        weather_data = self.get_new_data()
        if weather_data is not None:
            print('Reply received.')
            self._update_weather(weather_data['temp'], weather_data['main'], weather_data['description'], weather_data['icon'])
            print('Successfully updated.')
        else:
            print('No data received. Clearing display.')

    def _update_weather(self, temp: int, main: str, description: int, icon: str):
        self.weather_data.update(temp, main, description, icon)


class Weather:
    def __init__(self, parent_group):
        y = (int)(config['character_height'] + config['text_padding']) * (index + 1)

        self.line_label = Label(config['font'], max_glyphs=config['destination_max_characters'], anchor_point=(0, 0))
        self.line_label.x = 0
        self.line_label.y = y
        self.line_label.color = config['orange']
        self.line_label.text = config['loading_line_text'][:config['train_line_width']]

        self.car_label = Label(config['font'], max_glyphs=config['destination_max_characters'], anchor_point=(0, 0))
        self.car_label.x = 15
        self.car_label.y = y
        self.car_label.color = config['orange']
        self.car_label.text = config['loading_min_text'][:config['train_line_width']]

        self.destination_label = Label(config['font'], max_glyphs=config['destination_max_characters'],
                                       anchor_point=(0, 0))
        self.destination_label.x = 30
        self.destination_label.y = y
        self.destination_label.color = config['orange']
        self.destination_label.text = config['loading_destination_text'][:config['destination_max_characters']]

        self.min_label = Label(config['font'], max_glyphs=config['min_label_characters'], anchor_point=(0, 0))
        self.min_label.x = config['matrix_width'] - (config['min_label_characters'] * config['character_width']) - 2
        self.min_label.y = y
        self.min_label.color = config['orange']
        self.min_label.text = config['loading_min_text']

        self.group = displayio.Group(max_size=4)
        self.group.append(self.line_label)
        self.group.append(self.car_label)
        self.group.append(self.destination_label)
        self.group.append(self.min_label)

        parent_group.append(self.group)

    def show(self):
        self.group.hidden = False

    def hide(self):
        self.group.hidden = True

    def set_line(self, line: str, line_color: int):
        self.line_label.color = line_color
        self.line_label.text = line[:config['train_line_width']]

    def set_car(self, car_length: str, car_color: int):
        self.car_label.color = car_color
        self.car_label.text = car_length[:config['car_length_max_characters']]

    def set_destination(self, destination: str):
        self.destination_label.text = destination[:config['destination_max_characters']]

    def set_arrival_time(self, minutes: str):
        # Ensuring we have a string
        minutes = str(minutes)
        minutes_len = len(minutes)

        # Left-padding the minutes label
        minutes = ' ' * (config['min_label_characters'] - minutes_len) + minutes

        self.min_label.text = minutes

    def update(self, line: str, line_color: int, car_length: str, car_color: int, destination: str, minutes: str):
        self.show()
        self.set_line(line, line_color)
        self.set_car(car_length, car_color)
        self.set_destination(destination)
        self.set_arrival_time(minutes)
