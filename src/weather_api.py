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
        temp_color = WeatherApi._get_temp_color(temp)
        description = weather['current']['weather'][0]['main']
        tim = WeatherApi._get_time(weather['current']['dt'], weather['timezone_offset'])
        dt = WeatherApi._get_date(weather['current']['dt'], weather['timezone_offset'])
        chance_of_rain = str(WeatherApi._get_chance_of_rain(weather['minutely'])).split('.')[0]
        rain_color = WeatherApi._get_rain_color(chance_of_rain)
        return {
            'temp': temp,
            'temp_color': temp_color,
            'description': description,
            'time': tim,
            'date': dt,
            'chance_of_rain': chance_of_rain,
            'rain_color': rain_color
        }

    def _get_temp_color(temp: int) -> int:
        return config['red']

    def _get_rain_color(chance_of_rain: int) -> int:
        return config['blue']

    def _get_date(epoch_time: int, tz_offset: int) -> str:
        time_tup = time.localtime(epoch_time + tz_offset)
        mon_abrv = WeatherApi._get_mon_abrv(time_tup.tm_mon)
        return mon_abrv + ' ' + str(time_tup.tm_mday) + ', ' + str(time_tup.tm_year)[-2:]

    def _get_time(epoch_time: int, tz_offset: int) -> str:
        time_tup = time.localtime(epoch_time + tz_offset)
        str_min = str(time_tup.tm_min)
        hour = time_tup.tm_hour
        if len(str_min) == 1:
            str_min = '0' + str_min

        if time_tup.tm_isdst == 1:
            hour += 1
        ampm = 'am'
        if hour >= 12:
            ampm = 'pm'

        if hour > 12 and hour != 0:
            hour -= 12
        elif hour == 0:
            hour = 12

        str_hour = str(hour)

        if len(str_hour) != 2:
            str_hour = '0' + str_hour

        return str_hour + ':' + str_min + ampm

    def _get_mon_abrv(mon: int) -> str:
        dict = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
        }

        return dict.get(mon)

    def _get_chance_of_rain(predictions) -> int:
        total_chance = 0
        for prediction in predictions:
            total_chance += prediction['precipitation']
        return total_chance