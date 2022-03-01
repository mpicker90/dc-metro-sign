# DC Metro Board
import time
# import board
# import rgbmatrix
# import framebufferio
# import displayio

from config import config
from train_board import TrainBoard
from metro_api import MetroApi, MetroApiOnFireException

STATION_CODE = config['metro_station_code']
TRAIN_GROUP = config['train_group']
REFRESH_INTERVAL = config['refresh_interval']

# bit_depth = 1
# base_width = 64
# base_height = 32
# chain_across = 2
# tile_down = 1
# serpentine = True
#
# width = base_width * chain_across
# height = base_height * tile_down
#
# addr_pins = [board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD]
# rgb_pins = [
# 	board.MTX_R1,
# 	board.MTX_G1,
# 	board.MTX_B1,
# 	board.MTX_R2,
# 	board.MTX_G2,
# 	board.MTX_B2,
# ]
# clock_pin = board.MTX_CLK
# latch_pin = board.MTX_LAT
# oe_pin = board.MTX_OE
#
# displayio.release_displays()
# matrix = rgbmatrix.RGBMatrix(
# 	width=width,
# 	height=height,
# 	bit_depth=bit_depth,
# 	rgb_pins=rgb_pins,
# 	addr_pins=addr_pins,
# 	clock_pin=clock_pin,
# 	latch_pin=latch_pin,
# 	output_enable_pin=oe_pin,
# 	tile=tile_down, serpentine=serpentine,
# )
#
# displayio.release_displays()

#display = framebufferio.FramebufferDisplay(matrix)

def refresh_trains() -> [dict]:
	try:
		return MetroApi.fetch_train_predictions(STATION_CODE, TRAIN_GROUP)
	except MetroApiOnFireException:
		print('WMATA Api is currently on fire. Trying again later ...')
		return None

train_board = TrainBoard(refresh_trains)

while True:
	train_board.refresh()
	time.sleep(REFRESH_INTERVAL)
