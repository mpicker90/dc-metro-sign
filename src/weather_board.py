import displayio
import display_creator
from adafruit_display_text.label import Label
from config import config
import gc

class WeatherBoard:
    """
        get_new_data is a function that is expected to return a dictionarie like this:
            {
                'temp': '123'
                'main': rain,
                'description': 'thunder storms',
                'icon': 'd05'
                'location': 'Washington DC
                'timestamp': 12321312312
            }
    """

    def __init__(self, get_new_data):
        self.get_new_data = get_new_data
        self.display = display_creator.create_display()
        self.parent_group = displayio.Group(scale = 1, x = 0, y = 0)
        self.weather = Weather(self.parent_group)
        self.display.show(self.parent_group)

    def refresh(self) -> bool:
        print('Refreshing weather information...')
        weather_data = self.get_new_data()
        print(gc.mem_free())
        if weather_data is not None:
            print('Reply received.')
            self._update_weather(weather_data['temp'], 0, weather_data['description'], weather_data['time'])
            print('Successfully updated.')
        else:
            print('No data received. Clearing display.')

        self.display.show(self.parent_group)

    def _update_weather(self, temp: int, rain: int, description: str, time: int):
        self.weather.update(temp, 0, description, time)


class Weather:
    def __init__(self, parent_group):
        self.time_label = Label(config['font'], anchor_point=(0, 0))
        self.time_label.x = 10
        self.time_label.y = 12 + config['base_offset']
        self.time_label.color = config['orange']
        self.time_label.text = '00:00PM'

        self.temp_label = Label(config['font'], anchor_point=(0, 0))
        self.temp_label.x = 65
        self.temp_label.y = 2 + config['base_offset']
        self.temp_label.color = config['orange']
        self.temp_label.text = config['loading_line_text'][:config['train_line_width']]

        self.rain_label = Label(config['font'], anchor_point=(0, 0))
        self.rain_label.x = 92
        self.rain_label.y = 2 + config['base_offset']
        self.rain_label.color = config['orange']
        self.rain_label.text = '0% Rain'

        self.location_label = Label(config['font'], anchor_point=(0, 0))
        self.location_label.x = 20
        self.location_label.y = 23 + config['base_offset']
        self.location_label.color = config['orange']
        self.location_label.text = config['weather_location']

        self.description_label = Label(config['font'], anchor_point=(0, 0))
        self.description_label.x = 65
        self.description_label.y = 13 + config['base_offset']
        self.description_label.color = config['orange']
        self.description_label.text = config['loading_destination_text'][:config['destination_max_characters']]

        self.group = displayio.Group()
        self.group.append(self.time_label)
        self.group.append(self.rain_label)
        self.group.append(self.temp_label)
        self.group.append(self.location_label)
        self.group.append(self.description_label)

        parent_group.append(self.group)

    def show(self):
        self.group.hidden = False

    def hide(self):
        self.group.hidden = True

    def set_temp(self, temp: int):
        # Ensuring we have a string
        temp_str = str(temp)

        self.temp_label.color = config['orange']
        self.temp_label.text = temp_str.split('.')[0] + '°F'

    def set_rain(self, rain: str):
        self.rain_label.text = str(rain) + '% Rain'

    def set_description(self, description: str):
        self.description_label.text = description

    def set_time(self, time: str):
        self.time_label.text = str(time)

    def update(self, temp: int, rain: int, description: str, time: int):
        self.show()
        self.set_temp(temp)
        self.set_rain(rain)
        self.set_description(description)
        self.set_time(time)


    def scroll(self, line):
        line.x = line.x - 1
        line_width = line.bounding_box[2]
        if line.x < -line_width:
            line.x = self.display.width
