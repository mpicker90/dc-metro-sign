import displayio
import display_util
from adafruit_display_text import bitmap_label
from adafruit_display_shapes.rect import Rect
from config import config
import time


class TrainBoard:
    """
        get_new_data is a function that is expected to return an array of dictionaries like this:

        [
            {
                'line': 'OR'
                'line_color': 0xFFFFFF,
                'destination': 'Dest Str',
                'arrival': '5'
                'car_length': '6',
                'car_color': x0FFFFFF
            }
        ]
    """

    def __init__(self, get_new_data, display):
        self.get_new_data = get_new_data
        self.parent_group = displayio.Group()
        self.display = display

        self.header_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.header_label.color = config['red']
        self.header_label.text = "LN CAR  DEST      MIN"
        self.header_label.x = 1
        self.header_label.y = config['base_offset']

        self.wifi_rect = Rect(0, 31, 1, 1, fill=config['red'])
        self.bad_response_rect = Rect(1, 31, 1, 1, fill=config['off'])

        self.parent_group.append(self.header_label)
        self.parent_group.append(self.wifi_rect)
        self.parent_group.append(self.bad_response_rect)

        self.trains = []
        for i in range(config['num_trains']):
            self.trains.append(Train(self.parent_group, i))

    def refresh(self):
        print('Refreshing train information...')
        self.display.show(self.parent_group)
        self.bad_response_rect.fill = config['off']
        self.wifi_rect.fill = config['red']
        train_data = self.get_new_data()
        self.wifi_rect.fill = config['off']
        if train_data is not None:
            print('Reply received.')
            for i in range(config['num_trains']):
                if i < len(train_data):
                    train = train_data[i]
                    self._update_train(i, train['line'], train['line_color'], train['car_length'], train['car_color'],
                                       train['destination'], train['arrival'])
                else:
                    self._hide_train(i)

            print('Successfully updated.')
        else:
            print('No data received.')
            self.bad_response_rect.fill = config['blue']



    def _hide_train(self, index: int):
        self.trains[index].hide()

    def _update_train(self, index: int, line: str, line_color: int, car_length: str, car_color: int, destination: str,
                      minutes: str):
        self.trains[index].update(line, line_color, car_length, car_color, destination, minutes)

    def get_group(self):
        return self.parent_group

class Train:
    def __init__(self, parent_group, index):
        y = (int)(config['character_height'] + config['text_padding']) * (index + 1) + config['base_offset']

        self.line_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.line_label.x = 1
        self.line_label.y = y
        self.line_label.color = config['orange']
        self.line_label.text = config['loading_line_text'][:config['train_line_width']]

        self.car_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.car_label.x = 21
        self.car_label.y = y
        self.car_label.color = config['orange']
        self.car_label.text = config['loading_min_text'][:config['train_line_width']]

        self.destination_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.destination_label.x = 43
        self.destination_label.y = y
        self.destination_label.color = config['orange']
        self.destination_label.text = config['loading_destination_text'][:config['destination_max_characters']] + "    " + config['loading_min_text']

        self.group = displayio.Group()
        self.group.append(self.line_label)
        self.group.append(self.car_label)
        self.group.append(self.destination_label)

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

    def set_destination(self, destination: str, minutes: str):
        minutes_str = ' ' * (config['min_label_characters'] - len(minutes)) + str(minutes)
        dest = destination + (11 - len(destination)) * ' '
        self.destination_label.text = dest + minutes_str

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
        self.set_destination(destination, minutes)
