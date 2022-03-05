import board

from adafruit_matrixportal.network import Network

from config import config
from secrets import secrets


class WeatherApiOnFireException(Exception):
    pass


class WeatherApi:
    def fetch_weather_predictions(network) -> [dict]:
        return WeatherApi._fetch_weather_predictions(network=network, retry_attempt=0)

    def _fetch_weather_predictions(network, retry_attempt: int) -> [dict]:
        try:
            location = config['weather_location']
            units = "imperial"
            print("Getting weather for {}".format(location))
            api_url = (
                    config['weather_api_url'] + 'lat=' + config['weather_lat'] + '&lon=' + config['weather_lon'] + '&units=' + units + '&exclude=hourly,daily,alerts'
            )
            api_url += "&appid=" + secrets["openweather_token"]

            current_value = network.fetch(api_url).json()
            print(current_value)
            print('Received response from Weather api...')
            normalized_results = WeatherApi._normalize_weather_response(current_value)

            return normalized_results
        except RuntimeError:
            if retry_attempt < config['metro_api_retries']:
                print('Failed to connect to Weather API. Reattempting...')
                # Recursion for retry logic because I don't care about your stack
                return WeatherApi._fetch_weather_predictions(network, retry_attempt + 1)
            else:
                raise WeatherApiOnFireException()

    def _normalize_weather_response(weather: dict) -> dict:
        temp = weather['current']['temp']
        description = weather['current']['weather'][0]['description']
        time = weather['current']['dt']
        chance_of_rain = weather['minutely'][-1]['precipitation']
        return {
            'temp': temp,
            'description': description,
            'time': time,
            'chance_of_rain': chance_of_rain
        }