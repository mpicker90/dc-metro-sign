# DC Metro Board
import time
import displayio

from adafruit_display_text.label import Label
from adafruit_matrixportal.matrix import Matrix
from config import config
from train_board import TrainBoard
from metro_api import MetroApi, MetroApiOnFireException

STATION_CODE = config['metro_station_code']
TRAIN_GROUP = config['train_group']
REFRESH_INTERVAL = config['refresh_interval']

def refresh_trains() -> [dict]:
	try:
		return MetroApi.fetch_train_predictions(STATION_CODE, TRAIN_GROUP)
	except MetroApiOnFireException:
		print('WMATA Api is currently on fire. Trying again later ...')
		return None

display = Matrix().display
parent_group = displayio.Group(max_size=5)

try:
	train_board = TrainBoard(refresh_trains, display)
except Exception as e:
	print(e)


while True:
	try:
		train_board.refresh()
		time.sleep(REFRESH_INTERVAL)
	except Exception as e:
		print(e)
