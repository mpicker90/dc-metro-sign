from adafruit_bitmap_font import bitmap_font

config = {

    'auto_restart': True,
    'log_level': 'ERROR',
    'weather_display_time': 10,
    'train_display_time': 180,
    #########################
    # Metro Configuration   #
    #########################
    'station_list': [['C02', '2'], ['C02', '1'], ['E01', '1'], ['E01', '2'], ['A02', '1'], ['A02', '2']],

    #########################
    # Other Values You      #
    # Probably Shouldn't    #
    # Touch                 #
    #########################
    'metro_api_url': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',
    'weather_api_url': 'http://api.openweathermap.org/data/2.5/onecall?',
    'weather_location': 'Washington DC, US',
    'weather_lon': '-77.03217746105503',
    'weather_lat': '38.90688172534281',
    # Display Settings
    'matrix_width': 128,
    'num_trains': 3,
    'font': bitmap_font.load_font('6x10.bdf'),
    'min_label_characters': 3,
    'character_width': 6,
    'character_height': 7,
    'text_padding': 1,
    'base_offset': 3,

    'red': 0xFF0000,
    'orange': 0xFF5500,
    'yellow': 0xFFFF00,
    'green': 0x00FF00,
    'blue': 0x0000FF,
    'silver': 0xAAAAAA,
    'off': 0x000000,

    'station_map': {
        'C02': 'McPherson Square \nBL,OR,SV',
        'E01': 'Mt Vernon Sq 7th St \nGR,YL',
        'A02': 'Farragut North \nRD'
    }
}
