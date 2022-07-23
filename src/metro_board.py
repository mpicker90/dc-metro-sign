import gc

import displayio
from adafruit_display_text import bitmap_label
from config import config


def display(data):
    gc.collect()
    parent_group = displayio.Group()
    print("parent group created")
    header_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    header_label.color = config['red']
    header_label.text = "LN CAR  DEST      MIN"
    header_label.x = 1
    header_label.y = config['base_offset']
    print("header label created")
    parent_group.append(header_label)
    print("header label added")
    for i in range(config['num_trains']):
        if i < len(data):
            print("adding train ", gc.mem_free())
            parent_group.append(build_train(data[i], i))
            print("train added ", i)
            gc.collect()
    print("trains added")
    gc.collect()
    return parent_group


def build_train(datum, row):
    y = int(config['character_height'] + config['text_padding']) * (row + 1) + config['base_offset']
    line_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    line_label.x = 1
    line_label.y = y
    line_label.color = datum['line_color']
    line_label.text = datum['line']

    car_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    car_label.x = 21
    car_label.y = y
    car_label.color = datum['car_color']
    car_label.text = datum['car_length']

    minutes_str = ' ' * (config['min_label_characters'] - len(datum['arrival'])) + str(datum['arrival'])
    dest = datum['destination'] + (11 - len(datum['destination'])) * ' '

    destination_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    destination_label.x = 43
    destination_label.y = y
    destination_label.color = config['orange']
    destination_label.text = dest + minutes_str
    group = displayio.Group()

    group.append(line_label)
    group.append(car_label)
    group.append(destination_label)
    gc.collect()
    return group
    