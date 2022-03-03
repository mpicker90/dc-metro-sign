from config import config

# This file is required by the Matrix Portal library to properly
# initialize the WiFi chip on the board.
# 
# Why isn't aren't the SSID and password just parameters for the
# connect function? The world may never know :(
secrets = {
	'ssid': '2Gh wifi name here',
	'password': 'wifi password here',
	'metro_api_key': 'api key here'
}