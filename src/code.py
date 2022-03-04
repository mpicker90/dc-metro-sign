# DC Metro Board
import time
import board
import digitalio
import station_changer
import display_creator

from config import config
from train_board import TrainBoard
from metro_api import MetroApi, MetroApiOnFireException

STATION_LIST = config['station_list']
STATION_LIST_INDEX = 0
REFRESH_INTERVAL = config['refresh_interval']

# used to cycle stations
button_up = digitalio.DigitalInOut(board.BUTTON_UP)
button_up.direction = digitalio.Direction.INPUT
button_up.pull = digitalio.Pull.UP

button_down = digitalio.DigitalInOut(board.BUTTON_DOWN)
button_down.direction = digitalio.Direction.INPUT
button_down.pull = digitalio.Pull.UP

def refresh_trains() -> [dict]:
    global STATION_LIST
    global STATION_LIST_INDEX
    try:
        return MetroApi.fetch_train_predictions(STATION_LIST[STATION_LIST_INDEX][0],
                                                STATION_LIST[STATION_LIST_INDEX][1])
    except MetroApiOnFireException:
        print('WMATA Api is currently on fire. Trying again later ...')
        return None


def change_station():
    print('up button pressed, changing station')
    global STATION_LIST_INDEX
    global STATION_LIST
    global button_up
    global display
    STATION_LIST_INDEX = station_changer.change_station(STATION_LIST_INDEX, STATION_LIST, button_up)

try:
    train_board = TrainBoard(refresh_trains)
except Exception as e:
    print(e)

while True:
    if not button_up.value:
        change_station()
    try:
        train_board.refresh()
        time.sleep(REFRESH_INTERVAL)
    except Exception as e:
        print(e)
