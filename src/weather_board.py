import displayio
import time
import display_util
from adafruit_display_text import bitmap_label
from config import config

def display(data):
    parent_group = displayio.Group()

    parent_group.append(set_top_line(data))
    parent_group.append(set_date(data))
    parent_group.append(set_description(data))
    parent_group.append(set_location(data))

    return parent_group


def set_top_line(data):
    time_change = int(time.monotonic() - data['init_time'])
    current_time = int(data['time_sec'] + time_change)
    formatted_time = _get_time(current_time, data['time_offset'])
    rain_str = (' ' * (4 - len(data['rain']))) + str(data['rain']) + 'mm' + data['rain_icon']
    temp_str = data['temp'] + '°F' + data['temp_icon']

    top_line = formatted_time + "  " + temp_str + rain_str

    top_line_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    top_line_label.x = 2
    top_line_label.y = config['base_offset'] + 2
    top_line_label.color = config['orange']
    top_line_label.text = top_line
    return top_line_label

def set_description(data):
    description_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    description_label.x = display_util.right_center(data['description'])
    description_label.y = 13 + config['base_offset']
    description_label.color = config['orange']
    description_label.text = data['description']
    return description_label

def set_date(data):
    date_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    date_label.y = config['base_offset'] + 13
    date_label.color = config['orange']
    time_change = time.monotonic() - data['init_time']
    current_time = data['time_sec'] + time_change
    formatted_dt = _get_date(current_time, data['time_offset'])
    date_label.text = formatted_dt
    date_label.x = display_util.left_center(formatted_dt)
    return date_label

def set_location(data):
    location_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    location_label.x = display_util.center(config['weather_location'])
    location_label.y = 23 + config['base_offset']
    location_label.color = config['orange']
    location_label.text = config['weather_location']
    return location_label

def _get_mon_abrv(mon: int) -> str:
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


def _get_time(current_time: int, input_offset) -> str:
    time_tup = time.localtime(current_time + input_offset)
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


def _get_date(current_time: int, input_offset: int) -> str:
    time_tup = time.localtime(current_time + input_offset)
    mon_abrv = _get_mon_abrv(time_tup.tm_mon)
    return mon_abrv + ' ' + str(time_tup.tm_mday) + ', ' + str(time_tup.tm_year)[-2:]