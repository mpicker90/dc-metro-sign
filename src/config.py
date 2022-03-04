from adafruit_bitmap_font import bitmap_font

config = {
    #########################
    # Metro Configuration   #
    #########################
    'station_list': [['C02', '1'], ['C02', '2'], ['E01', '1'], ['E01', '2'], ['A02', '1'], ['A02', '2']],

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

    'line_header': 'LN',
    'car_header': 'CAR',
    'destination_header': 'DEST',
    'min_header': 'MIN',

    'loading_destination_text': 'Loading',
    'loading_min_text': '---',
    'loading_line_text': '--',

    'train_line_height': 6,
    'train_line_width': 2,

    'car_length_max_characters': 3,
    'min_label_characters': 3,
    'destination_max_characters': 16,

    'red': 0xFF0000,
    'orange': 0xFF5500,
    'yellow': 0xFFFF00,
    'green': 0x00FF00,
    'blue': 0x0000FF,
    'silver': 0xAAAAAA,

    'station_map': {
        'C02': 'McPherson Square',
        'A02': 'Farragut North',
        'C03': 'Farragut West',
        'E01': 'Mt Vernon Sq 7th'
    }
}
