// VERSION 1.0.1
#include <SPI.h>
#include <Wire.h>
#include <MAX30105.h>

#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_SSD1306.h>

MAX30105 particleSensor;

Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

long unblockedValue;  // Average IR at power up

String multiplyChar(char c, int n) {
  String result = "";
  for (int i = 0; i < n; i++) {
    result += c;
  }
  return result;
}

void displayMeasurement(int rLevel) {
  tft.fillScreen(ST77XX_BLACK);
  tft.setCursor(0, 30);

  int calibratedReading = f(rLevel);

  if (rLevel == 0) {
    tft.setTextColor(ST77XX_RED);
    tft.setTextSize(2);
    tft.print("Please load sample!");
    return;
  }

  tft.setTextColor(ST77XX_BLUE);
  tft.setTextSize(3);
  tft.print("real: ");
  tft.println(rLevel);
  tft.print("agtron: ");
  tft.println(calibratedReading);

  Serial.println("real:" + String(rLevel));
  Serial.println("agtron:" + String(calibratedReading));
  Serial.println("===========================");
}

int f(int x) {
  int intersectionPoint = 117;
  float deviation = 0.165;

  return round(x - (intersectionPoint - x) * deviation);
}

void setup() {
  Serial.begin(9600);
  Serial.print(F("Start Loading App"));

  Wire.begin();

  // turn on backlite
  pinMode(TFT_BACKLITE, OUTPUT);
  digitalWrite(TFT_BACKLITE, HIGH);

  // turn on the TFT / I2C power supply
  pinMode(TFT_I2C_POWER, OUTPUT);
  digitalWrite(TFT_I2C_POWER, HIGH);
  delay(10);

  // initialize TFT
  tft.init(135, 240); // Init ST7789 240x135
  tft.setRotation(3);
  tft.fillScreen(ST77XX_BLACK);

  Serial.println(F("TFT Initialized"));

  // Initialize sensor
  if (particleSensor.begin(Wire, I2C_SPEED_FAST) == false)  // Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1)
      ;
  }

  // The variable below calibrates the LED output on your hardware.
  byte ledBrightness = 135;

  byte sampleAverage = 4;  // Options: 1, 2, 4, 8, 16, --32--
  byte ledMode = 2;        // Options: 1 = Red only, --2 = Red + IR--, 3 = Red + IR + Green
  int sampleRate = 50;     // Options: 50, 100, 200, 400, 800, 1000, 1600, --3200--
  int pulseWidth = 411;    // Options: 69, 118, 215, --411--
  int adcRange = 16384;    // Options: 2048, --4096--, 8192, 16384

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);  // Configure sensor with these settings

  particleSensor.setPulseAmplitudeRed(0);
  particleSensor.setPulseAmplitudeGreen(0);

  particleSensor.disableSlots();
  particleSensor.enableSlot(2, 0x02);  // Enable only SLOT_IR_LED = 0x02

  // Update to ignore readings under 30.000
  unblockedValue = 30000;
}

void loop() {
  int rLevel = particleSensor.getIR();
  long currentDelta = rLevel - unblockedValue;

  if (currentDelta > (long)100) {
    displayMeasurement(rLevel / 1000);
  } else {
    displayMeasurement(0);
  }
  delay(100);
}