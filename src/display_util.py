import gc

import displayio
import board
import rgbmatrix
import framebufferio
import logger
from config import config

def create_display():
    try:
        bit_depth = 2
        base_width = 64
        base_height = 32
        chain_across = 2
        tile_down = 1
        serpentine = True

        width = base_width * chain_across
        height = base_height * tile_down

        addr_pins = [board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD]
        rgb_pins = [
            board.MTX_R1,
            board.MTX_G1,
            board.MTX_B1,
            board.MTX_R2,
            board.MTX_G2,
            board.MTX_B2,
        ]
        clock_pin = board.MTX_CLK
        latch_pin = board.MTX_LAT
        oe_pin = board.MTX_OE

        displayio.release_displays()
        matrix = rgbmatrix.RGBMatrix(
            width=width,
            height=height,
            bit_depth=bit_depth,
            rgb_pins=rgb_pins,
            addr_pins=addr_pins,
            clock_pin=clock_pin,
            latch_pin=latch_pin,
            output_enable_pin=oe_pin,
            tile=tile_down, serpentine=serpentine,
        )
        display = framebufferio.FramebufferDisplay(matrix)
        return display
    except Exception as e:
        print(e)


def _center_offset(base_offset: int, matrix_width_mod: int, text: str):
    return int(base_offset + ((((config['matrix_width'] / matrix_width_mod) - base_offset) / 2) - (
                (len(text) * config['character_width']) / 2)))


def left_center(text: str):
    return _center_offset(0, 2, text)


def right_center(text: str):
    return _center_offset(64, 1, text)


def center(text: str):
    return _center_offset(0, 1, text)


def turn_off_display(current_time):
    gc.collect()
    if 'display_off_time' in config and len(
            config['display_off_time'].split(":")) == 2 and 'display_on_time' in config and len(
            config['display_on_time'].split(":")) == 2:
        logger.debug("display time off is configured")
        display_off_hr = int(config['display_off_time'].split(":")[0])
        display_off_min = int(config['display_off_time'].split(":")[1])
        display_on_hr = int(config['display_on_time'].split(":")[0])
        display_on_min = int(config['display_on_time'].split(":")[1])
        logger.debug(f"display off {display_off_hr} {display_off_min}")
        logger.debug(f"display on {display_on_hr} {display_on_min}")
        logger.debug(f"current time {current_time.tm_hour} {current_time.tm_min}")
        if current_time.tm_hour >= display_off_hr and current_time.tm_min >= display_off_min:
            logger.debug("Time to shut down")
            if display_off_hr > display_on_hr:
                display_on_hr += 24
            if display_off_min > display_on_min:
                display_on_min += 60
            display_off_for_seconds = ((display_on_hr - display_off_hr) * 60 * 60) + ((display_on_min - display_off_min) * 60)
            logger.debug(f"display off time: {display_off_for_seconds}")
            gc.collect()
            return display_off_for_seconds
    gc.collect()
    return 0
