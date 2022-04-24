# DC Metro Board
import time
import board
import digitalio
import gc

import display_util
from adafruit_matrixportal.network import Network
from microcontroller import watchdog as w
from watchdog import WatchDogMode

from secrets import secrets

from config import config
import metro_board
import weather_board
import weather_api
import station_changer
from pong_board import PongBoard
from metro_api import MetroApi, MetroApiOnFireException
from weather_api import WeatherApiOnFireException

try:
    w.feed()
except Exception as e:
    print("watcher not set up")

network = Network(status_neopixel=board.NEOPIXEL)

network.fetch("http://example.com")

display = display_util.create_display()

STATION_LIST = config['station_list']
STATION_LIST_INDEX = 0

# used to cycle stations
button_up = digitalio.DigitalInOut(board.BUTTON_UP)
button_up.direction = digitalio.Direction.INPUT
button_up.pull = digitalio.Pull.UP

button_down = digitalio.DigitalInOut(board.BUTTON_DOWN)
button_down.direction = digitalio.Direction.INPUT
button_down.pull = digitalio.Pull.UP

w_timeout = 15
w.timeout = w_timeout
w.mode = WatchDogMode.RESET

w.feed()

def refresh_loop(wait_time: int):
    global STATION_LIST_INDEX
    i = 0
    while i < wait_time:
        w.feed()
        i += 1
        while not button_up.value:
            STATION_LIST_INDEX, parent_group = station_changer.update(STATION_LIST, STATION_LIST_INDEX)
            display.show(parent_group)
            time.sleep(1)
        if not button_down.value:
            gc.collect()
            PongBoard(display, w)
        time.sleep(1)


def refresh_trains() -> [dict]:
    return _refresh_trains(0)


def _refresh_trains(i: int):
    global STATION_LIST
    global STATION_LIST_INDEX
    try:
        return MetroApi.fetch_train_predictions(STATION_LIST[STATION_LIST_INDEX][0],
                                                STATION_LIST[STATION_LIST_INDEX][1], network)
    except MetroApiOnFireException:
        print('WMATA Api is currently on fire. Trying again later ...')
        handle_bad_requests(i)
        return _refresh_trains(i + 1)


def refresh_weather() -> [dict]:
    return _refresh_weather(0)


def _refresh_weather(i: int) -> [dict]:
    try:
        return weather_api.fetch_weather_predictions(network)
    except WeatherApiOnFireException:
        print('Weather Api is currently on fire. Trying again later ...')
        handle_bad_requests(i)
        return _refresh_weather(i + 1)


def handle_bad_requests(reset_times):
    global network
    if reset_times >= 3:
        print("To many retries restarting")
        time.sleep(w_timeout + 10)

    print("Bad response reattempting connection")
    w.feed()
    network._wifi.esp.reset()
    network._wifi.esp.connect(secrets)


gc.collect()
print(gc.mem_free())
while True:
    weather_board_time = time.time()
    data = refresh_weather()
    gc.collect()

    print(gc.mem_free())

    while time.time() - weather_board_time <= 180:
        w.feed()
        try:
            gc.collect()
            display.show(weather_board.display(data))
            refresh_loop(1)
            gc.collect()
            print(gc.mem_free())
        except Exception as e:
            print("error occurred in weather_board")
            print(e)

    train_board_time = time.time()
    while time.time() - train_board_time <= 300:
        try:
            gc.collect()
            display.show(metro_board.display(refresh_trains()))
            gc.collect()
            print(gc.mem_free())
        except Exception as e:
            print("error occurred in train_board")
            print(e)
        refresh_loop(15)
