import time
import sys
import board
import busio
from digitalio import DigitalInOut

import adafruit_ssd1306
import qwiic_max3010x


def runExample():
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

    print("Create the SSD1306 OLED class")
    # The first two parameters are the pixel width and pixel height.  Change these
    # to the right size for your display!
    # The I2C address for these displays is 0x3d or 0x3c, change to match
    # A reset line may be required if there is no auto-reset circuitry
    # , addr=0x3C
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    while True:
        rLevel = sensor.getIR()
        currentDelta = rLevel - unblockedValue
        output = 0

        if currentDelta > 100:
            output = rLevel / 1000

        print(output)
        display.fill(0)
        display.text(str(output), 0, 0, 1)
        display.show()


        time.sleep(0.1)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)


