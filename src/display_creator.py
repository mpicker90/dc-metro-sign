import displayio
import board
import rgbmatrix
import framebufferio

from adafruit_matrixportal.matrix import Matrix

def create_display():
    try:
        bit_depth = 4
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