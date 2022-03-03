from adafruit_bitmap_font import bitmap_font

config = {
	#########################
	# Metro Configuration   #
	#########################

	# Metro Station Code
	# TODO UPDATE ME

	'metro_station_code': 'C02',

	# Metro Train Group
	# TODO UPDATE ME
	'train_group': '2',

	#########################
	# Other Values You      #
	# Probably Shouldn't    #
	# Touch                 #
	#########################
	'metro_api_url': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',
	'metro_api_retries': 2,
	'refresh_interval': 5,

	# Display Settings
	'matrix_width': 128,
	'num_trains': 3,
	'font': bitmap_font.load_font('lib/5x7.bdf'),

	'character_width': 4,
	'character_height': 7,
	'text_padding': 1,

	'loading_destination_text': 'Loading',
	'loading_min_text': '---',
	'loading_line_text': '--',

	'train_line_height': 6,
	'train_line_width': 2,

	'car_length_max_characters': 3,
	'min_label_characters': 3,
	'destination_max_characters': 12,

	'red': 0xFF0000,
	'orange': 0xFF5500,
	'yellow': 0xFFFF00,
	'green': 0x00FF00,
	'blue': 0x0000FF,
	'silver': 0xAAAAAA

}