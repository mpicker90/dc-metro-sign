import displayio
import time
import display_util
from adafruit_display_text import bitmap_label
from adafruit_display_shapes.rect import Rect
from config import config


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

    def __init__(self, get_new_data, display):
        self.description = None
        self.rain = None
        self.temp = None
        self.get_new_data = get_new_data
        self.display = display
        self.wifi_rect = Rect(0, 31, 1, 1, fill=config['red'])
        self.bad_response_rect = Rect(1, 31, 1, 1, fill=config['off'])
        self.initial_time = time.monotonic()
        self.input_time = 0

        self.input_offset = 0

        self.top_line_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.top_line_label.x = 2
        self.top_line_label.y = config['base_offset'] + 2
        self.top_line_label.color = config['orange']
        self.top_line_label.text = '00:00PM  00°F    0mm♀'

        self.date_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.date_label.x = display_util.left_center('Jan 01, 00')
        self.date_label.y = config['base_offset'] + 13
        self.date_label.color = config['orange']
        self.date_label.text = 'Jan 01, 00'

        self.description_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.description_label.x = display_util.right_center(config['loading_destination_text'])
        self.description_label.y = 13 + config['base_offset']
        self.description_label.color = config['orange']
        self.description_label.text = config['loading_destination_text']

        self.location_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.location_label.x = display_util.center(config['weather_location'])
        self.location_label.y = 23 + config['base_offset']
        self.location_label.color = config['orange']
        self.location_label.text = config['weather_location']

        self.parent_group = displayio.Group()
        self.parent_group.append(self.top_line_label)
        self.parent_group.append(self.date_label)
        self.parent_group.append(self.description_label)
        self.parent_group.append(self.location_label)
        self.parent_group.append(self.wifi_rect)
        self.parent_group.append(self.bad_response_rect)

    def refresh(self):
        print('Refreshing weather information...')
        self.display.show(self.parent_group)
        self.bad_response_rect.fill = config['off']
        self.wifi_rect.fill = config['red']
        weather_data = self.get_new_data()
        self.wifi_rect.fill = config['off']
        if weather_data is not None:
            print('Reply received.')
            print(weather_data)
            self.update(weather_data['temp'], weather_data['chance_of_rain'],
                        weather_data['description'],
                        weather_data['time_sec'], weather_data['time_offset'])
            print('Successfully updated.')
        else:
            self.bad_response_rect.fill = config['blue']
            print('No data received.')

    def update_time(self):
        self.set_top_line()
        self.set_date()

    def show(self):
        self.parent_group.hidden = False

    def hide(self):
        self.parent_group.hidden = True

    def set_top_line(self):
        time_change = int(time.monotonic() - self.initial_time)
        current_time = int(self.input_time + time_change)
        formatted_time = self._get_time(current_time)
        rain_str = (' ' * (5 - len(self.rain))) + str(self.rain) + 'mm♀'
        temp_str = self.temp.split('.')[0] + '°F'

        top_line = formatted_time + "  " + temp_str + rain_str

        self.top_line_label.text = top_line

    def set_middle_line(self):
        self.set_date()
        self.set_description()

    def update(self, temp: int, rain: int, description: str, time_sec: int, time_offset: int):
        self.show()
        if time_sec is not None:
            self.input_time = time_sec
            self.input_offset = time_offset
        if rain is not None:
            self.rain = rain
        if temp is not None:
            self.temp = temp
        if description is not None:
            self.description = description

        self.initial_time = time.monotonic()
        self.set_top_line()
        self.set_middle_line()

    def set_description(self):
        self.description_label.text = self.description

    def set_date(self):
        time_change = time.monotonic() - self.initial_time
        current_time = self.input_time + time_change
        formatted_dt = self._get_date(current_time)
        self.date_label.text = formatted_dt
        display_util.left_center(formatted_dt)

    def _get_date(self, current_time: int) -> str:
        time_tup = time.localtime(current_time + self.input_offset)
        mon_abrv = self._get_mon_abrv(time_tup.tm_mon)
        return mon_abrv + ' ' + str(time_tup.tm_mday) + ', ' + str(time_tup.tm_year)[-2:]

    def _get_mon_abrv(self, mon: int) -> str:
        dict = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
        }

        return dict.get(mon)

    def _get_time(self, current_time: int,) -> str:
        time_tup = time.localtime(current_time + self.input_offset)
        str_min = str(time_tup.tm_min)
        hour = time_tup.tm_hour
        if len(str_min) == 1:
            str_min = '0' + str_min

        if time_tup.tm_isdst == 1:
            hour += 1
        ampm = 'am'
        if hour >= 12:
            ampm = 'pm'

        if hour > 12 and hour != 0:
            hour -= 12
        elif hour == 0:
            hour = 12

        str_hour = str(hour)

        if len(str_hour) != 2:
            str_hour = '0' + str_hour

        return str_hour + ':' + str_min + ampm
