import gc

import displayio
import logger
from adafruit_display_text import bitmap_label
from config import config


def display(data):
    gc.collect()
    parent_group = displayio.Group()
    header_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    header_label.color = config['red']
    header_label.text = "LN CAR  DEST      MIN"
    header_label.x = 2 #1
    header_label.y = config['base_offset']
    parent_group.append(header_label)
    first_train_over_wait_time = -1
    for i in range(len(data)):
        logger.error(data[i])
        wait_time = data[i]['arrival']
        if wait_time == "ARR" or wait_time == "BRD":
            wait_time = 0
        if int(wait_time) >= config['min_wait_time']:
            first_train_over_wait_time = i
            break

    remainder = len(data) - 1 - first_train_over_wait_time

    if remainder <= config['num_trains']:
        first_train_over_wait_time -= remainder
        if first_train_over_wait_time < 0:
            first_train_over_wait_time = 0

    for i in range(config['num_trains']):
        if i + first_train_over_wait_time < len(data):
            logger.mem("adding train")
            parent_group.append(build_train(data[i + first_train_over_wait_time], i))
            logger.debug(f"train added {i}")
            gc.collect()
    logger.debug("trains added")
    gc.collect()
    return parent_group


def build_train(datum, row):
    group = displayio.Group()
    destination_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))

    y = int(config['character_height'] + config['text_padding']) * (row + 1) + config['base_offset']
    line_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
    line_label.x = 2 #1
    line_label.y = y
    line_label.color = datum['line_color']
    line_label.text = datum['line']

    minutes_str = ' ' * (config['min_label_characters'] - len(datum['arrival'])) + str(datum['arrival'])
    dest = datum['destination'] + (11 - len(datum['destination'])) * ' '

    if datum['car_length'] == '8':
        car_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        car_label.x = 20  # 21
        car_label.y = y
        car_label.color = datum['car_color']
        car_label.text = datum['car_length']
        group.append(car_label)
        destination_label.x = 44
    else:
        dest = datum['car_length'] + "   " + dest
        destination_label.x = 20  # 43

    destination_label.y = y
    destination_label.color = config['orange']
    destination_label.text = dest + minutes_str

    group.append(line_label)
    group.append(destination_label)
    gc.collect()
    return group
    