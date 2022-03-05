import board

from adafruit_matrixportal.network import Network

from config import config
from secrets import secrets


class WeatherApiOnFireException(Exception):
    pass


class WeatherApi:

    def fetch_weather_predictions(network) -> str:
        return WeatherApi._fetch_weather_predictions(network=network, retry_attempt=0)

    def _fetch_weather_predictions(network, retry_attempt: int) -> [dict]:
        try:
            location = config['weather_location']
            units = "imperial"
            print("Getting weather for {}".format(location))
            api_url = (
                    config['weather_api_url'] + 'lat=' + config['weather_lat'] + '&lon=' + config['weather_lon'] + '&units=' + units + '&exclude=current,hourly,daily,alerts'
            )
            api_url += "&appid=" + secrets["openweather_token"]
            value = network.fetch(api_url).text()
            print(value)
            print('Received response from Weather api...')

            return value['minutely'][-1]['precipitation']
        except RuntimeError:
            if retry_attempt < config['metro_api_retries']:
                print('Failed to connect to Weather API. Reattempting...')
                # Recursion for retry logic because I don't care about your stack
                return WeatherApi._fetch_weather_predictions(network, retry_attempt + 1)
            else:
                raise WeatherApiOnFireException()

    def fetch_current_weather(network) -> [dict]:
        return WeatherApi._fetch_current_weather(network=network, retry_attempt=0)

    def _fetch_current_weather(network, retry_attempt: int) -> [dict]:
        try:
            location = config['weather_location']
            units = "imperial"
            print("Getting weather for {}".format(location))
            api_url = (
                    config['weather_api_url'] + 'lat=' + config['weather_lat'] + '&lon=' + config['weather_lon'] + '&units=' + units + '&exclude=minutely,hourly,daily,alerts'
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
       # chance_of_rain = weather['hourly'][0]['precipitation']
        return {
            'temp': temp,
            'description': description,
            'time': time,
           # 'chance_of_rain': chance_of_rain
        }

    # def dada(self):
    #     var = {'lat': 38.8951,
    #            'timezone_offset': -18000,
    #            'current': {
    #                'dt': 1646444412,
    #                'sunrise': 1646393783,
    #                'visibility': 10000,
    #                'weather': [
    #                    {
    #                     'id': 803,
    #                     'icon': '04n',
    #                     'main': 'Clouds',
    #                     'description': 'broken clouds'
    #                     }
    #                ],
    #                'pressure': 1030,
    #                'humidity': 52,
    #                'clouds': 75,
    #                'wind_deg': 120,
    #                'wind_speed': 8.05,
    #                'temp': 37.38,
    #                'dew_point': 22.59,
    #                'feels_like': 31.37,
    #                'sunset': 1646435018,
    #                'uvi': 0
    #            },
    #            'minutely': [
    #                {
    #                 'precipitation': 0,
    #                 'dt': 1646444460
    #                 },
    #                {'precipitation': 0, 'dt': 1646444520}, {'precipitation': 0, 'dt': 1646444580}, {'precipitation': 0, 'dt': 1646444640}, {'precipitation': 0, 'dt': 1646444700}, {'precipitation': 0, 'dt': 1646444760}, {'precipitation': 0, 'dt': 1646444820}, {'precipitation': 0, 'dt': 1646444880}, {'precipitation': 0, 'dt': 1646444940}, {'precipitation': 0, 'dt': 1646445000}, {'precipitation': 0, 'dt': 1646445060}, {'precipitation': 0, 'dt': 1646445120}, {'precipitation': 0, 'dt': 1646445180}, {'precipitation': 0, 'dt': 1646445240}, {'precipitation': 0, 'dt': 1646445300}, {'precipitation': 0, 'dt': 1646445360}, {'precipitation': 0, 'dt': 1646445420}, {'precipitation': 0, 'dt': 1646445480}, {'precipitation': 0, 'dt': 1646445540}, {'precipitation': 0, 'dt': 1646445600}, {'precipitation': 0, 'dt': 1646445660}, {'precipitation': 0, 'dt': 1646445720}, {'precipitation': 0, 'dt': 1646445780}, {'precipitation': 0, 'dt': 1646445840}, {'precipitation': 0, 'dt': 1646445900}, {'precipitation': 0, 'dt': 1646445960}, {'precipitation': 0, 'dt': 1646446020}, {'precipitation': 0, 'dt': 1646446080}, {'precipitation': 0, 'dt': 1646446140}, {'precipitation': 0, 'dt': 1646446200}, {'precipitation': 0, 'dt': 1646446260}, {'precipitation': 0, 'dt': 1646446320}, {'precipitation': 0, 'dt': 1646446380}, {'precipitation': 0, 'dt': 1646446440}, {'precipitation': 0, 'dt': 1646446500}, {'precipitation': 0, 'dt': 1646446560}, {'precipitation': 0, 'dt': 1646446620}, {'precipitation': 0, 'dt': 1646446680}, {'precipitation': 0, 'dt': 1646446740}, {'precipitation': 0, 'dt': 1646446800}, {'precipitation': 0, 'dt': 1646446860}, {'precipitation': 0, 'dt': 1646446920}, {'precipitation': 0, 'dt': 1646446980}, {'precipitation': 0, 'dt': 1646447040}, {'precipitation': 0, 'dt': 1646447100}, {'precipitation': 0, 'dt': 1646447160}, {'precipitation': 0, 'dt': 1646447220}, {'precipitation': 0, 'dt': 1646447280}, {'precipitation': 0, 'dt': 1646447340}, {'precipitation': 0, 'dt': 1646447400}, {'precipitation': 0, 'dt': 1646447460}, {'precipitation': 0, 'dt': 1646447520}, {'precipitation': 0, 'dt': 1646447580}, {'precipitation': 0, 'dt': 1646447640}, {'precipitation': 0, 'dt': 1646447700}, {'precipitation': 0, 'dt': 1646447760}, {'precipitation': 0, 'dt': 1646447820}, {'precipitation': 0, 'dt': 1646447880}, {'precipitation': 0, 'dt': 1646447940}, {'precipitation': 0, 'dt': 1646448000}, {'precipitation': 0, 'dt': 1646448060}], 'lon': -77.0364, 'timezone': 'America/New_York'}
    #
    #
