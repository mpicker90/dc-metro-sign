import board
import openweather_graphics

from adafruit_matrixportal.network import Network

from config import config
from secrets import secrets

# Keeping a global reference for this
_network = Network(status_neopixel=board.NEOPIXEL)


class WeatherApiOnFireException(Exception):
    pass


class WeatherApi:

    def fetch_weather_predictions(self) -> [dict]:
        return WeatherApi._fetch_train_predictions(retry_attempt=0)

    def fetch_weather_predictions(self, retry_attempt: int) -> [dict]:
        try:
            location = config['weather_location']
            units = "imperial"
            print("Getting weather for {}".format(location))
            api_url = (
                    config['weather_api_url'] + location + "&units=" + units
            )
            api_url += "&appid=" + secrets["openweather_token"]

            value = _network.fetch(api_url).json()

            print(value)
            print('Received response from Weather api...')

            normalized_results = map(WeatherApi._normalize_weather_response, value)
            print(normalized_results)
            return normalized_results
        except RuntimeError:
            if retry_attempt < config['metro_api_retries']:
                print('Failed to connect to Weather API. Reattempting...')
                # Recursion for retry logic because I don't care about your stack
                return WeatherApi._fetch_weather_predictions(retry_attempt + 1)
            else:
                raise WeatherApiOnFireException()

    def _normalize_weather_response(weather: dict) -> dict:

        temp = weather['main']['temp']
        main = weather[0]['weather']['main']
        description = weather[0]['weather']['description']
        icon = weather[0]['weather']['icon']

        return {
            'temp': temp,
            'main': main,
            'description': description,
            'icon': icon
        }
