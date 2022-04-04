import displayio
import display_util
from adafruit_display_text import bitmap_label
from adafruit_display_shapes.rect import Rect
from config import config
import time


class PongBoard:
    def __init__(self, display):
        self.parent_group = displayio.Group()
        self.display = display

        self.score_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.score_label.x = display_util.center("0")
        self.score_label.y = 2 + config['base_offset']
        self.score_label.color = config['silver']
        self.score_label.text = "0"

        self.ball_label = Rect(10, 10, 2, 2, fill=config['silver'])

        self.paddle_label = Rect(2, 14, 2, 5, fill=config['silver'])

        self.parent_group.append(self.score_label)
        self.parent_group.append(self.ball_label)
        self.parent_group.append(self.paddle_label)
        self.display.show(self.parent_group)
        i = 10
        while True:
            print(i)
            i += 1
            self.ball_label = Rect(i, 10, 2, 2, fill=config['silver'])
            self.parent_group.append(self.ball_label)
