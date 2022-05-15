import displayio
from config import config
from adafruit_display_text import bitmap_label


def update(station_list, index):
    station_list = station_list

    parent_group = displayio.Group()

    label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    label.color = config['red']
    label.text = config['station_map'][station_list[0][0]]
    label.x = 1
    label.y = 4

    parent_group.append(label)

    index += 1
    if index >= len(station_list):
        index = 0
    label.text = config['station_map'][station_list[index][0]] + "\n" + station_list[index][1]

    return index, parent_group

