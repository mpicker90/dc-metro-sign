import displayio
import board
import rgbmatrix
import framebufferio

from adafruit_display_text.label import Label
from adafruit_matrixportal.matrix import Matrix

from config import config


class TrainBoard:
    """
        get_new_data is a function that is expected to return an array of dictionaries like this:

        [
            {
                'line_color': 0xFFFFFF,
                'destination': 'Dest Str',
                'arrival': '5'
            }
        ]
    """

    def __init__(self, get_new_data, display):
        self.get_new_data = get_new_data

        self.parent_group = displayio.Group(max_size=5)

        self.heading_line_label = Label(config['font'], max_glyphs=len(config['heading_text']), anchor_point=(0, 0))
        self.heading_line_label.color = config['heading_color']
        self.heading_line_label.text = 'LN'
        self.heading_line_label.x = 0

        self.heading_car_label = Label(config['font'], max_glyphs=len(config['heading_text']), anchor_point=(0, 0))
        self.heading_car_label.color = config['heading_color']
        self.heading_car_label.text = 'CAR'
        self.heading_car_label.x = 12

        self.heading_dest_label = Label(config['font'], max_glyphs=len(config['heading_text']), anchor_point=(0, 0))
        self.heading_dest_label.color = config['heading_color']
        self.heading_dest_label.text = 'DEST'
        self.heading_dest_label.x = 29

        self.heading_min_label = Label(config['font'], max_glyphs=len(config['heading_text']), anchor_point=(0, 0))
        self.heading_min_label.color = config['heading_color']
        self.heading_min_label.text = 'MIN'
        self.heading_min_label.x = 50

        self.header_group = displayio.Group(max_size=4)
        self.header_group.append(self.heading_line_label)
        self.header_group.append(self.heading_car_label)
        self.header_group.append(self.heading_dest_label)
        self.header_group.append(self.heading_min_label)


        self.heading_label = Label(config['font'], max_glyphs=len(config['heading_text']), anchor_point=(0, 0))
        self.heading_label.color = config['heading_color']
        self.heading_label.text = config['heading_text']
        # self.parent_group.append(self.heading_label)

        self.parent_group.append(self.header_group)


        self.trains = []
        for i in range(config['num_trains']):
            self.trains.append(Train(self.parent_group, i))

        display.show(self.parent_group)

    def refresh(self) -> bool:
        print('Refreshing train information...')
        train_data = self.get_new_data()
        if train_data is not None:
            print('Reply received.')
            for i in range(config['num_trains']):
                if i < len(train_data):
                    train = train_data[i]
                    self._update_train(i, train['line'], train['line_color'], train['car_length'], train['car_color'], train['destination'], train['arrival'])
                else:
                    self._hide_train(i)

            print('Successfully updated.')
        else:
            print('No data received. Clearing display.')

            for i in range(config['num_trains']):
                self._hide_train(i)

    def _hide_train(self, index: int):
        self.trains[index].hide()

    def _update_train(self, index: int, line: str, line_color: int, car_length: str, car_color: int, destination: str, minutes: str):
        self.trains[index].update(line, line_color, car_length, car_color, destination, minutes)


class Train:
    def __init__(self, parent_group, index):
        y = (int)(config['character_height'] + config['text_padding']) * (index + 1)

        self.line_label = Label(config['font'], max_glyphs=config['destination_max_characters'],  anchor_point=(0, 0))
        self.line_label.x = 0
        self.line_label.y = y
        self.line_label.color = config['text_color']
        self.line_label.text = config['loading_line_text'][:config['train_line_width']]

        self.car_label = Label(config['font'], max_glyphs=config['destination_max_characters'],  anchor_point=(0, 0))
        self.car_label.x = 12
        self.car_label.y = y
        self.car_label.color = config['text_color']
        self.car_label.text = config['loading_min_text'][:config['train_line_width']]

        self.destination_label = Label(config['font'], max_glyphs=config['destination_max_characters'], anchor_point=(0, 0))
        self.destination_label.x = 19
        self.destination_label.y = y
        self.destination_label.color = config['text_color']
        self.destination_label.text = config['loading_destination_text'][:config['destination_max_characters']]

        self.min_label = Label(config['font'], max_glyphs=config['min_label_characters'], anchor_point=(0, 0))
        self.min_label.x = config['matrix_width'] - (config['min_label_characters'] * config['character_width']) + 1
        self.min_label.y = y
        self.min_label.color = config['text_color']
        self.min_label.text = config['loading_min_text']

        self.group = displayio.Group(max_size=4)
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
