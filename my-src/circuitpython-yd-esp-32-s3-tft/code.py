import time
import sys
import board
import busio
from digitalio import DigitalInOut

import qwiic_max3010x

import terminalio
import displayio

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

from adafruit_display_text import label
from adafruit_st7789 import ST7789


def runExample():
    # First set some parameters used for shapes and text
    BORDER = 20
    FONTSCALE = 2
    BACKGROUND_COLOR = 0x00FF00  # Bright Green
    FOREGROUND_COLOR = 0xAA0088  # Purple
    TEXT_COLOR = 0xFFFF00
    
    # Release any resources currently in use for the displays
    displayio.release_displays()

    spi = board.SPI()
    tft_cs = board.TFT_CS
    tft_dc = board.TFT_DC

    display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
    display = ST7789(
        display_bus, rotation=90, width=240, height=135, rowstart=40, colstart=53
    )
    
    # Make the display context
    splash = displayio.Group()
    display.root_group = splash

    color_bitmap = displayio.Bitmap(display.width, display.height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = BACKGROUND_COLOR

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(
        display.width - BORDER * 2, display.height - BORDER * 2, 1
    )
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(
        inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
    )
    splash.append(inner_sprite)

    # Draw a label
    text = "Hello World!"
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_width = text_area.bounding_box[2] * FONTSCALE
    text_group = displayio.Group(
        scale=FONTSCALE,
        x=display.width // 2 - text_width // 2,
        y=display.height // 2,
    )
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    
    
    print("\nSparkFun MAX3010x Photodetector - Example 1\n")
    sensor = qwiic_max3010x.QwiicMax3010x()

    if sensor.begin() == False:
        print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    else:
        print("The Qwiic MAX3010x is connected.")

    # The variable below calibrates the LED output on your hardware.
    ledBrightness = 135

    sampleAverage = 4  # Options: 1, 2, 4, 8, 16, --32--
    ledMode = 2        # Options: 1 = Red only, --2 = Red + IR--, 3 = Red + IR + Green
    sampleRate = 50    # Options: 50, 100, 200, 400, 800, 1000, 1600, --3200--
    pulseWidth = 411   # Options: 69, 118, 215, --411--
    adcRange = 16384   # Options: 2048, --4096--, 8192, 16384
    unblockedValue = 30000

    if sensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange) == False:
        print("Device setup failure. Please check your connection", \
            file=sys.stderr)
        return
    else:
        sensor.setPulseAmplitudeRed(0)
        sensor.setPulseAmplitudeGreen(0)
        sensor.disableSlots()
        sensor.enableSlot(2, 0x02)
        print("Setup complete.")

    print("Create the I2C interface")
    #i2c = busio.I2C(board.SCL, board.SDA)
    i2c = board.I2C()

    while True:
        rLevel = sensor.getIR()
        currentDelta = rLevel - unblockedValue
        output = 0

        if currentDelta > 100:
            output = rLevel / 1000

        print(output)
        
        # Draw a label
        splash.remove(text_group)
        text = str(output)
        text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
        text_width = text_area.bounding_box[2] * FONTSCALE
        text_group = displayio.Group(
            scale=FONTSCALE,
            x=display.width // 2 - text_width // 2,
            y=display.height // 2,
        )
        text_group.append(text_area)  # Subgroup for text scaling]
        splash.append(text_group)


        time.sleep(0.2)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)


