import time
import board
import digitalio
import displayio
import display_creator
from config import config

from adafruit_display_text.label import Label


def change_station(index, station_list, button):
    display = display_creator.create_display()
    while not button.value:
        index += 1
        if index >= len(station_list):
            index = 0
        print(str(index) + ' ' + station_list[index][0] + ' ' + station_list[index][1])
        print(config['station_map'][station_list[index][0]])
        parent_group = displayio.Group()

        station_label = Label(config['font'], anchor_point=(0, 0))
        station_label.color = config['red']
        station_label.text = config['station_map'][station_list[index][0]] + ' ' + station_list[index][1]
        station_label.x = 10
        station_label.y = 16

        parent_group.append(station_label)
        display.show(parent_group)

        time.sleep(1)
    return index
