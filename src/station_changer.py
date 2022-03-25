import time
import displayio
from config import config
from adafruit_display_text import bitmap_label

class Station_Changer:
    def __init__(self, station_list, button, display):
        self.station_list = station_list
        self.button = button
        self.display = display
        self.parent_group = displayio.Group()

        self.station_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.station_label.color = config['red']
        self.station_label.text = config['station_map'][station_list[0][0]]
        self.station_label.x = 1
        self.station_label.y = 4

        self.platform_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.platform_label.color = config['red']
        self.platform_label.text = station_list[0][1]
        self.platform_label.x = 2
        self.platform_label.y = 14

        self.parent_group.append(self.station_label)
        self.parent_group.append(self.platform_label)

    def change_station(self, index):
        self.display.show(self.parent_group)
        while not self.button.value:
            index += 1
            if index >= len(self.station_list):
                index = 0
            self.station_label.text = config['station_map'][self.station_list[index][0]]
            self.platform_label.text = self.station_list[index][1]
            time.sleep(1)
        return index

    def get_group(self):
        return self.parent_group
