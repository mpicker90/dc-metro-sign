import displayio
import digitalio
from adafruit_debug_i2c import DebugI2C
import busio
import display_util
import adafruit_lis3dh

import logger
import watcher_util
from adafruit_display_text import bitmap_label
from config import config
import time
import board


class PongBoard:
    def __init__(self, display):
        self.i2c = DebugI2C(busio.I2C(board.SCL, board.SDA))
        self.int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
        self.accelerometer = adafruit_lis3dh.LIS3DH_I2C(self.i2c, address=0x19, int1=self.int1)
        self.parent_group = displayio.Group()
        self.display = display

        self.score_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.score_label.x = display_util.center("0")
        self.score_label.y = 2 + config['base_offset']
        self.score_label.color = config['silver']
        self.score_label.text = "0"

        self.ball_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.ball_label.x = 10
        self.ball_label.y = 14
        self.ball_label.color = config['silver']
        self.ball_label.text = "ó"

        self.paddle_label = bitmap_label.Label(config['font'], anchor_point=(0, 0))
        self.paddle_label.x = 2
        self.paddle_label.y = 14
        self.paddle_label.color = config['silver']
        self.paddle_label.text = "ò"

        self.parent_group.append(self.score_label)
        self.parent_group.append(self.ball_label)
        self.parent_group.append(self.paddle_label)
        self.display.show(self.parent_group)

        self.x_movement = 1
        self.y_movement = -1
        self.score = 0
        self.sleep_time = 0.05
        self.previous_x_accel = 0
        self.previous_y_accel = 0
        self.previous_z_accel = 0

        while True:
            self.move_paddle()
            self.move_ball()
            time.sleep(self.sleep_time)
            watcher_util.feed()

    def move_paddle(self):
        acc_x, acc_y, acc_z = self.accelerometer.acceleration

        if acc_z > 1.5:
            move = 1
            if acc_z > 3:
                move = 2
            if self.paddle_label.y <= 30:
                self.paddle_label.y = self.paddle_label.y + move

        if acc_z < -1.5:
            move = 1
            if acc_z < -3:
                move = 2
            if self.paddle_label.y > 4:
                self.paddle_label.y = self.paddle_label.y - move

        self.previous_x_accel = acc_x
        self.previous_y_accel = acc_y
        self.previous_z_accel = acc_z

    def move_ball(self):
        if self.hit_back_wall():
            self.x_movement = self.x_movement * -1
            self.ball_label.x = 126

        if self.hit_paddle():
            logger.debug("hit paddle")
            self.x_movement = self.x_movement * -1
            self.score += 1
            self.score_label.text = str(self.score)
            if self.sleep_time > 0.01:
                self.sleep_time = self.sleep_time - 0.01

        if self.hit_ceiling():
            logger.debug("hit ceiling")
            self.y_movement = self.y_movement * -1
            self.ball_label.y = 4

        if self.hit_floor():
            logger.debug("hit floor")
            self.y_movement = self.y_movement * -1
            self.ball_label.y = 34

        if self.hit_player_wall():
            logger.debug("hit player wall")
            self.ball_label.x = 10
            self.score = 0
            self.score_label.text = str(self.score)
            self.x_movement = 1
            self.y_movement = 1
            self.sleep_time = 0.05
            return

        self.ball_label.x += self.x_movement
        self.ball_label.y += self.y_movement

    def hit_back_wall(self):
        if self.ball_label.x >= 126 and self.x_movement > 0:
            return True
        return False

    def hit_player_wall(self):
        if self.ball_label.x <= 0 and self.x_movement < 0:
            return True
        return False

    def hit_paddle(self):
        if self.paddle_label.x < self.ball_label.x < self.paddle_label.x + 2:
            if self.paddle_label.y - 2 < self.ball_label.y < self.paddle_label.y + 5:
                return True
        return False

    def hit_ceiling(self):
        if self.ball_label.y <= 4:
            return True
        return False

    def hit_floor(self):
        if self.ball_label.y >= 34:
            return True
        return False
