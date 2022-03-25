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
        self.get_new_data = get_new_data
        self.display = display
        self.wifi_rect = Rect(0, 31, 1, 1, fill=config['red'])
        self.bad_response_rect = Rect(1, 31, 1, 1, fill=config['off'])
        self.initial_time = time.monotonic()
        self.input_time = 0

        self.input_offset = 0
        self.time_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.time_label.x = 2
        self.time_label.y = config['base_offset'] + 2
        self.time_label.color = config['orange']
        self.time_label.text = '00:00PM'

        self.date_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.date_label.x = display_util.left_center('Jan 01, 00')
        self.date_label.y = config['base_offset'] + 13
        self.date_label.color = config['orange']
        self.date_label.text = 'Jan 01, 00'

        self.temp_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.temp_label.x = display_util.center('00°F')
        self.temp_label.y = 2 + config['base_offset']
        self.temp_label.color = config['orange']
        self.temp_label.text = '00°F'

        self.rain_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.rain_label.x = 90
        self.rain_label.y = 2 + config['base_offset']
        self.rain_label.color = config['orange']
        self.rain_label.text = '  0mm♀'

        self.location_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.location_label.x = display_util.center(config['weather_location'])
        self.location_label.y = 23 + config['base_offset']
        self.location_label.color = config['orange']
        self.location_label.text = config['weather_location']

        self.description_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.description_label.x = display_util.right_center(config['loading_destination_text'])
        self.description_label.y = 13 + config['base_offset']
        self.description_label.color = config['orange']
        self.description_label.text = config['loading_destination_text']

        self.parent_group = displayio.Group()
        self.parent_group.append(self.time_label)
        self.parent_group.append(self.rain_label)
        self.parent_group.append(self.temp_label)
        self.parent_group.append(self.location_label)
        self.parent_group.append(self.description_label)
        self.parent_group.append(self.date_label)
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
            self.update(weather_data['temp'], weather_data['chance_of_rain'],
                                 weather_data['description'],
                                 weather_data['time_sec'], weather_data['time_offset'])
            print('Successfully updated.')
        else:
            self.bad_response_rect.fill = config['blue']
            print('No data received.')


    def update_time(self):
        self.weather.update_time()
        return self.weather

    def get_group(self):
        return self.parent_group

    def show(self):
        self.parent_group.hidden = False

    def hide(self):
        self.parent_group.hidden = True

    def set_temp(self, temp: int):
        temp_str = str(temp)
        self.temp_label.text = temp_str.split('.')[0] + '°F'

    def set_rain(self, rain: str):
        while len(rain) != 3:
            rain = ' ' + rain
        self.rain_label.text = str(rain) + 'mm♀'

    def set_description(self, description: str):
        self.description_label.x = display_util.right_center(description)
        self.description_label.text = description

    def set_time(self, time_sec: int, time_offset: int):
        time_change = int(time.monotonic() - self.initial_time)
        current_time = int(time_sec + time_change)
        formatted_time = self._get_time(current_time, time_offset)
        self.time_label.text = formatted_time

    def set_date(self, time_sec: int, time_offset: int):
        time_change = time.monotonic() - self.initial_time
        current_time = time_sec + time_change
        formatted_dt = self._get_date(current_time, time_offset)
        self.date_label.text = formatted_dt
        display_util.left_center(formatted_dt)

    def update(self, temp: int, rain: int, description: str, time_sec: int, time_offset: int):
        self.show()
        if time_sec is not None:
            self.input_time = time_sec
            self.input_offset = time_offset
        self.set_temp(temp)
        self.set_rain(rain)
        self.set_description(description)
        self.initial_time = time.monotonic()
        self.set_time(time_sec, time_offset)
        self.set_date(time_sec, time_offset)

    def update_time(self):
        self.set_time(self.input_time, self.input_offset)
        self.set_date(self.input_time, self.input_offset)

    def _get_date(self, epoch_time: int, tz_offset: int) -> str:
        time_tup = time.localtime(epoch_time + tz_offset)
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

    def _get_time(self, epoch_time: int, tz_offset: int) -> str:
        time_tup = time.localtime(epoch_time + tz_offset)
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