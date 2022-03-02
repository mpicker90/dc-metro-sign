from adafruit_bitmap_font import bitmap_font

config = {
	#########################
	# Network Configuration #
	#########################

	# WIFI Network SSID
	# TODO UPDATE ME
	'wifi_ssid': 'TP-Link_6B00',

	# WIFI Password
	# TODO UPDATE ME
	'wifi_password': '87427783',

	#########################
	# Metro Configuration   #
	#########################

	# Metro Station Code
	# TODO UPDATE ME

	'metro_station_code': 'C02',

	# Metro Train Group
	# TODO UPDATE ME
	'train_group': '2',

	# API Key for WMATA
	# TODO UPDATE ME
	'metro_api_key': '79a96eab26874765a170006dcf33bd04',
	#########################
	# Other Values You      #
	# Probably Shouldn't    #
	# Touch                 #
	#########################
	'metro_api_url': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',
	'metro_api_retries': 2,
	'refresh_interval': 5, # 5 seconds is a good middle ground for updates, as the processor takes its sweet ol time

	# Display Settings
	'matrix_width': 64,
	'num_trains': 3,
	'font': bitmap_font.load_font('lib/5x7.bdf'),

	'character_width': 4,
	'character_height': 7,
	'text_padding': 1,
	'text_color': 0xFF7500,

	'loading_destination_text': 'Loading',
	'loading_min_text': '---',
	'loading_line_text': '--',
	'loading_line_color': 0xFF00FF, # Something something Purple Line joke

	'heading_text': 'LN CAR DEST    MIN',
	'heading_color': 0xFF0000,

	'train_line_height': 6,
	'train_line_width': 2,

	'car_length_max_characters': 3,
	'min_label_characters': 3,
	'destination_max_characters': 6,
}