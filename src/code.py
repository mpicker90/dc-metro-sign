from adafruit_matrixportal.network import Network

import time
import board
import digitalio
import displayio
import gc

import metro_board
import logger
import weather_board
import weather_api
import station_changer
import watcher_util
import display_util

from pong_board import PongBoard
from metro_api import MetroApi, MetroApiOnFireException
from weather_api import WeatherApiOnFireException
from secrets import secrets
from config import config

logger.mem("Init")
display = display_util.create_display()
display.root_group = displayio.Group()
logger.mem("After display")

try:
    watcher_util.feed()
except Exception as e:
    logger.debug("watcher not set up")

try:
    network = Network(status_neopixel=board.NEOPIXEL)
    network.fetch("http://example.com")
except Exception as e:
    logger.error(e)
    watcher_util.force_restart()

logger.mem("After Network")
STATION_LIST = config['station_list']
STATION_LIST_INDEX = 0

# used to cycle stations
button_up = digitalio.DigitalInOut(board.BUTTON_UP)
button_up.direction = digitalio.Direction.INPUT
button_up.pull = digitalio.Pull.UP

button_down = digitalio.DigitalInOut(board.BUTTON_DOWN)
button_down.direction = digitalio.Direction.INPUT
button_down.pull = digitalio.Pull.UP

watcher_util.setup_watcher()

def refresh_loop(wait_time: int):
    global STATION_LIST_INDEX
    i = 0
    button_pressed = False

    while i < wait_time:
        watcher_util.feed()
        i += 1
        while not button_up.value:
            button_pressed = True
            STATION_LIST_INDEX, parent_group = station_changer.update(STATION_LIST, STATION_LIST_INDEX)
            display.root_group = parent_group
            time.sleep(1)
        if not button_down.value:
            gc.collect()
            PongBoard(display)
        time.sleep(1)
        if button_pressed:
            break


def refresh_trains(i: int = 0):
    global STATION_LIST
    global STATION_LIST_INDEX
    try:
        return MetroApi.fetch_train_predictions(STATION_LIST[STATION_LIST_INDEX][0],
                                                STATION_LIST[STATION_LIST_INDEX][1], network)
    except MetroApiOnFireException:
        logger.error('WMATA Api is currently on fire. Trying again later ...')
        handle_bad_requests(i)
        return refresh_trains(i + 1)


def refresh_weather(i: int = 0) -> [dict]:
    try:
        return weather_api.fetch_weather_predictions(network)
    except WeatherApiOnFireException:
        logger.error('Weather Api is currently on fire. Trying again later ...')
        handle_bad_requests(i)
        return refresh_weather(i + 1)


def handle_bad_requests(reset_times):
    global network
    if reset_times >= 3:
        logger.error("To many retries restarting")
        watcher_util.force_restart()

    logger.error("Bad response reattempting connection")
    watcher_util.feed()
    network._wifi.esp.disconnect()
    network._wifi.esp.connect(secrets)
    network._wifi.esp.reset()
    network.fetch("http://example.com")
    watcher_util.feed()


gc.collect()
logger.mem("pre main loop")
while True:
    weather_board_time = time.time()
    data = refresh_weather()
    gc.collect()

    logger.mem("after weather call")
    while time.time() - weather_board_time <= config['weather_display_time']:
        watcher_util.feed()
        try:
            gc.collect()
            display.root_group = weather_board.display(data)
            gc.collect()
        except Exception as e:
            logger.error("error occurred in weather_board")
            logger.error(e)
        refresh_loop(1)

    train_board_time = time.time()
    while time.time() - train_board_time <= config['train_display_time']:
        try:
            gc.collect()
            logger.mem("before metro call")
            display.root_group = metro_board.display(refresh_trains())
            logger.mem("after metro call")
            gc.collect()
        except Exception as e:
            logger.error("error occurred in metro_board")
            logger.error(e)
        refresh_loop(config['train_api_wait_time'])

    display.root_group = displayio.Group()
    gc.collect()
    try:
        current_time = time.localtime(
            int(data['time_sec'] + (int(time.monotonic() - data['init_time']))) + data['time_offset'])
        display_off_time = display_util.turn_off_display(current_time)
        if display_off_time > 0:
            refresh_loop(display_off_time)
            on_time = time.localtime(
                int(data['time_sec'] + (int(time.monotonic() - data['init_time']))) + data['time_offset'])
            logger.debug(f"turning display on at {on_time}")
    except Exception as e:
        logger.error("error occurred turning off display")
        logger.error(e)
