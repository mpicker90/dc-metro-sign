from config import config
from secrets import secrets

class MetroApiOnFireException(Exception):
    pass

class MetroApi:
    def fetch_train_predictions(station_code: str, group: str, network) -> [dict]:
        return MetroApi._fetch_train_predictions(station_code, group, network, retry_attempt=0)

    def _fetch_train_predictions(station_code: str, group: str, network, retry_attempt: int) -> [dict]:
        try:
            api_url = config['metro_api_url'] + station_code
            train_data = network.fetch(api_url, headers={
                'api_key': secrets['metro_api_key']
            }).json()

            print('Received response from WMATA api...')

            trains = filter(lambda t: t['Group'] == group, train_data['Trains'])

            normalized_results = list(map(MetroApi._normalize_train_response, trains))

            return normalized_results
        except RuntimeError as e:
            print('Failed to connect to WMATA API.')
            print(e)
            raise MetroApiOnFireException()

    def _normalize_train_response(train: dict) -> dict:
        line = train['Line']
        destination = train['Destination']
        arrival = train['Min']
        car = train['Car']

        if destination == 'No Passenger' or destination == 'NoPssenger' or destination == 'ssenger':
            destination = 'No Psngr'

        return {
            'line_color': MetroApi._get_line_color(line),
            'line': line,
            'destination': destination,
            'arrival': arrival,
            'car_length': car,
            'car_color': MetroApi._get_car_color(car)
        }

    def _get_line_color(line: str) -> int:
        if line == 'RD':
            return config['red']
        elif line == 'OR':
            return config['orange']
        elif line == 'YL':
            return config['yellow']
        elif line == 'GR':
            return config['green']
        elif line == 'BL':
            return config['blue']
        else:
            return config['silver']

    def _get_car_color(car: str) -> int:
        if car == '6':
            return config['orange']
        else:
            return config['green']
