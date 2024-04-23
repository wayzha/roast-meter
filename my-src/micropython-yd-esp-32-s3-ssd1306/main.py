import time
import sys
import machine

import qwiic_max3010x
from ssd1306 import SSD1306_I2C

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
    i2c = machine.I2C(sda=machine.Pin(23), scl=machine.Pin(22))

    print("Create the SSD1306_I2C class")
    display = SSD1306_I2C(128, 32, i2c)

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


