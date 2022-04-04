# DC Metro Board
import time
import board
import digitalio
import gc

import display_util
from adafruit_matrixportal.network import Network
from microcontroller import watchdog as w
from watchdog import WatchDogMode

from config import config
from metro_board import TrainBoard
from weather_board import WeatherBoard
from pong_board import PongBoard
from station_changer import Station_Changer
from metro_api import MetroApi, MetroApiOnFireException
from weather_api import WeatherApi, WeatherApiOnFireException

print("start: " + str(gc.mem_free()))
network = Network(status_neopixel=board.NEOPIXEL)
network.fetch("http://example.com")
print("network: " + str(gc.mem_free()))
display = display_util.create_display()
print("display: " + str(gc.mem_free()))
STATION_LIST = config['station_list']
STATION_LIST_INDEX = 0

# used to cycle stations
button_up = digitalio.DigitalInOut(board.BUTTON_UP)
button_up.direction = digitalio.Direction.INPUT
button_up.pull = digitalio.Pull.UP

button_down = digitalio.DigitalInOut(board.BUTTON_DOWN)
button_down.direction = digitalio.Direction.INPUT
button_down.pull = digitalio.Pull.UP

w.timeout = 15
w.mode = WatchDogMode.RESET


def refresh_loop(wait_time: int):
    global STATION_LIST_INDEX
    global train_board
    global weather_board
    global w

    i = 0
    while i < wait_time:
        w.feed()
        i += 1
        try:
            weather_board.update_time()
        except Exception as e:
            print(e)
        if not button_up.value:
            STATION_LIST_INDEX = station_changer_board.change_station(STATION_LIST_INDEX)
        if not button_down.value:
            train_board = None
            weather_board = None
            gc.collect()
            PongBoard(display, w)
        time.sleep(1)


def refresh_trains() -> [dict]:
    global STATION_LIST
    global STATION_LIST_INDEX
    try:
        return MetroApi.fetch_train_predictions(STATION_LIST[STATION_LIST_INDEX][0],
                                                STATION_LIST[STATION_LIST_INDEX][1], network)
    except MetroApiOnFireException:
        print('WMATA Api is currently on fire. Trying again later ...')
        return None


def refresh_weather() -> [dict]:
    try:
        return WeatherApi.fetch_weather_predictions(network)
    except WeatherApiOnFireException:
        print('Weather Api is currently on fire. Trying again later ...')
        return None


print("pre boards: " + str(gc.mem_free()))
train_board = TrainBoard(refresh_trains, display)
print("train board: " + str(gc.mem_free()))
weather_board = WeatherBoard(refresh_weather, display)
print("weather boards: " + str(gc.mem_free()))
station_changer_board = Station_Changer(STATION_LIST, button_up, display)
print("station changer: " + str(gc.mem_free()))

while True:
    try:
        print(gc.mem_free())
        gc.collect()
        print(gc.mem_free())
        weather_board.refresh()
    except Exception as e:
        print("error occurred in weather_board")
        print(e)
    refresh_loop(120)

    train_board_time = time.time()
    while time.time() - train_board_time <= 300:
        try:
            print(gc.mem_free())
            gc.collect()
            print(gc.mem_free())
            train_board.refresh()
        except Exception as e:
            print("error occurred in train_board")
            print(e)
        refresh_loop(5)
