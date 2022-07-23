# DC Metro Board
import time
import board
import digitalio
import gc

import display_util
from adafruit_matrixportal.network import Network

from secrets import secrets

from config import config
import metro_board
import logger
import weather_board
import weather_api
import station_changer
import watcher_util
from pong_board import PongBoard
from metro_api import MetroApi, MetroApiOnFireException
from weather_api import WeatherApiOnFireException

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
            display.show(parent_group)
            time.sleep(1)
        if not button_down.value:
            gc.collect()
            PongBoard(display)
        time.sleep(1)
        if button_pressed:
            break


def refresh_trains() -> [dict]:
    return _refresh_trains(0)


def _refresh_trains(i: int):
    global STATION_LIST
    global STATION_LIST_INDEX
    try:
        return MetroApi.fetch_train_predictions(STATION_LIST[STATION_LIST_INDEX][0],
                                                STATION_LIST[STATION_LIST_INDEX][1], network)
    except MetroApiOnFireException:
        logger.error('WMATA Api is currently on fire. Trying again later ...')
        handle_bad_requests(i)
        return _refresh_trains(i + 1)


def refresh_weather() -> [dict]:
    return _refresh_weather(0)


def _refresh_weather(i: int) -> [dict]:
    try:
        return weather_api.fetch_weather_predictions(network)
    except WeatherApiOnFireException:
        logger.error('Weather Api is currently on fire. Trying again later ...')
        handle_bad_requests(i)
        return _refresh_weather(i + 1)


def handle_bad_requests(reset_times):
    global network
    if reset_times >= 3:
        logger.error("To many retries restarting")
        watcher_util.force_restart()

    logger.info("Bad response reattempting connection")
    watcher_util.feed()
    network._wifi.esp.reset()
    network._wifi.esp.connect(secrets)
    network.fetch("http://example.com")
    watcher_util.feed()


gc.collect()
logger.mem("pre main loop")
while True:
    # weather_board_time = time.time()
    # data = refresh_weather()
    # gc.collect()
    #
    # logger.mem("after weather call")
    # while time.time() - weather_board_time <= 120:
    #     watcher_util.feed()
    #     try:
    #         gc.collect()
    #         display.show(weather_board.display(data))
    #         refresh_loop(1)
    #         gc.collect()
    #     except Exception as e:
    #         logger.error("error occurred in weather_board")
    #         logger.error(e)

    train_board_time = time.time()
    while time.time() - train_board_time <= 180:
        try:
            gc.collect()
            logger.mem("before metro call")
            display.show(metro_board.display(refresh_trains()))
            logger.mem("after metro call")
            gc.collect()
        except Exception as e:
            logger.error("error occurred in metro_board")
            logger.error(e)
        refresh_loop(15)
