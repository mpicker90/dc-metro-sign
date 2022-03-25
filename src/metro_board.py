import displayio
import display_util
from adafruit_display_text import bitmap_label
from adafruit_display_shapes.rect import Rect
from config import config


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
        self.heading_line_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.heading_line_label.color = config['red']
        self.heading_line_label.text = config['line_header']
        self.heading_line_label.x = 0
        self.heading_line_label.y = config['base_offset']

        self.heading_car_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.heading_car_label.color = config['red']
        self.heading_car_label.text = config['car_header']
        self.heading_car_label.x = 18
        self.heading_car_label.y = config['base_offset']

        self.heading_dest_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.heading_dest_label.color = config['red']
        self.heading_dest_label.text = config['destination_header']
        self.heading_dest_label.x = 49
        self.heading_dest_label.y = config['base_offset']

        self.heading_min_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.heading_min_label.color = config['red']
        self.heading_min_label.text = config['min_header']
        self.heading_min_label.x = config['matrix_width'] - (
                    config['min_label_characters'] * config['character_width']) - 2
        self.heading_min_label.y = config['base_offset']

        self.header_group = displayio.Group()
        self.header_group.append(self.heading_line_label)
        self.header_group.append(self.heading_car_label)
        self.header_group.append(self.heading_dest_label)
        self.header_group.append(self.heading_min_label)

        self.wifi_rect = Rect(0, 31, 1, 1, fill=config['red'])
        self.bad_response_rect = Rect(1, 31, 1, 1, fill=config['off'])

        self.parent_group.append(self.header_group)
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
        self.line_label.x = 0
        self.line_label.y = y
        self.line_label.color = config['orange']
        self.line_label.text = config['loading_line_text'][:config['train_line_width']]

        self.car_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.car_label.x = 20
        self.car_label.y = y
        self.car_label.color = config['orange']
        self.car_label.text = config['loading_min_text'][:config['train_line_width']]

        self.destination_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.destination_label.x = 41
        self.destination_label.y = y
        self.destination_label.color = config['orange']
        self.destination_label.text = config['loading_destination_text'][:config['destination_max_characters']]

        self.min_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.min_label.x = config['matrix_width'] - (config['min_label_characters'] * config['character_width']) - 2
        self.min_label.y = y
        self.min_label.color = config['orange']
        self.min_label.text = config['loading_min_text']

        self.group = displayio.Group()
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