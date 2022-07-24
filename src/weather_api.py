import time

import logger
from config import config
from secrets import secrets
import gc


class WeatherApiOnFireException(Exception):
    pass


def fetch_weather_predictions(network) -> [dict]:
    try:
        location = config['weather_location']
        units = "imperial"
        logger.debug("Getting weather for {}".format(location))
        api_url = (
                config['weather_api_url'] + 'lat=' + config['weather_lat'] + '&lon=' + config[
            'weather_lon'] + '&units=' + units + '&exclude=hourly,daily,alerts'
        )
        api_url += "&appid=" + secrets["openweather_token"]
        current_value = network.fetch(api_url).json()
        logger.info('Received response from Weather api...')
        logger.debug(current_value)
        normalized_results = _normalize_weather_response(current_value)
        current_value = None
        gc.collect()
        return normalized_results
    except Exception as e:
        logger.error('Failed to connect to Weather API.')
        logger.error(e)
        raise WeatherApiOnFireException()


def _normalize_weather_response(weather: dict) -> dict:
    if 'current' in weather:
        temp = str(weather['current']['temp']).split('.')[0]
        temp_icon = _get_temp_icon(weather['current']['temp'])
        description = weather['current']['weather'][0]['main']
        if description == 'Thunderstorm':
            description = 'Thunder'
        time_sec = weather['current']['dt']
    else:
        temp = "--"
        temp_icon = 'ø'
        description = "--"
        time_sec = None

    time_offset = weather['timezone_offset']

    if 'minutely' in weather:
        chance_of_rain = str(_get_chance_of_rain(weather['minutely'])).split('.')[0]
        rain_icon = _get_rain_icon(_get_chance_of_rain(weather['minutely']))
    else:
        chance_of_rain = "--"
        rain_icon = 'ô'

    if 'hourly' in weather:
        chance_of_rain = str(weather['hourly'][0]['pop'])

    formatted_response = {
        'temp': temp,
        'temp_icon': temp_icon,
        'description': description,
        'time_sec': time_sec,
        'init_time': time.monotonic(),
        'time_offset': time_offset,
        'rain': chance_of_rain,
        'rain_icon': rain_icon
    }
    logger.debug(formatted_response)
    return formatted_response


def _get_chance_of_rain(predictions) -> int:
    total_chance = 0
    for prediction in predictions:
        total_chance += prediction['precipitation']
    return total_chance


def _get_temp_icon(temp) -> str:
    if temp <= 32:
        return 'ø'
    elif temp <= 60:
        return '÷'
    elif temp <= 80:
        return 'ö'
    else:
        return 'õ'


def _get_rain_icon(rain) -> str:
    if rain <= 10:
        return 'ô'
    else:
        return '♀'
