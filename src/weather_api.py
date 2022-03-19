import time

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
            print('Received response from Weather api...')
            normalized_results = WeatherApi._normalize_weather_response(current_value)

            return normalized_results
        except RuntimeError as e:
            print('Failed to connect to Weather API.')
            print(e)
            raise WeatherApiOnFireException()

    def _normalize_weather_response(weather: dict) -> dict:
        temp = str(weather['current']['temp']).split('.')[0]
        description = weather['current']['weather'][0]['main']
        time_sec =weather['current']['dt']
        time_offset = weather['timezone_offset']

        if 'minutely' in weather:
                chance_of_rain = str(WeatherApi._get_chance_of_rain(weather['minutely'])).split('.')[0]
        else:
            chance_of_rain = "--"

        return {
            'temp': temp,
            'description': description,
            'time_sec': time_sec,
            'time_offset': time_offset,
            'chance_of_rain': chance_of_rain,
        }

    def _get_chance_of_rain(predictions) -> int:
        total_chance = 0
        for prediction in predictions:
            total_chance += prediction['precipitation']
        return total_chance