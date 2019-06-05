#include <Adafruit_NeoPixel.h>

#define NUMPIXELS 256
#define NUMSTRIPS 16

//Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, 2, NEO_GRB + NEO_KHZ800);

Adafruit_NeoPixel strips[NUMSTRIPS] = {
    Adafruit_NeoPixel(NUMPIXELS, 0, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 1, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 2, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 3, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 4, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 5, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 7, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 9, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 10, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 11, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 12, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 14, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 15, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 16, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 17, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(NUMPIXELS, 18, NEO_GRB + NEO_KHZ800)
};

void setup() {
  Serial.begin(2000000);
  for (int i = 0; i < NUMSTRIPS; i++) {
    strips[i].begin();
    strips[i].setBrightness(75);
    strips[i].show();
  }
}


void loop() {
  if (Serial.available()) {
    getNewFrame();
  }
  
//  else {
//    /// REQUEST NEW FRAME
//    /// THIS DOESN'T SEEM TO ADD ANY EFFICIENCY
//    Serial.write('r');
//  }

  

}


void getNewFrame() {
    
    char received = Serial.read();
    if (received == 's') {
      while (!Serial.available());
      int r = Serial.read();
      while (!Serial.available());
      int g = Serial.read();
      while (!Serial.available());
      int b = Serial.read();
      while (!Serial.available());
      int col = Serial.read();
      while (!Serial.available());
      int led = Serial.read();

      strips[col].setPixelColor(led, strips[col].Color(r, g, b));

    }

    if (received == 'f') { /// SHOW FRAME
      for (int i = 0; i < NUMSTRIPS; i++) {
        strips[i].show();
      }
    }

    if (received == 'c') { /// CLEAR ALL
      for (int i = 0; i < NUMSTRIPS; i++) {
        strips[i].clear();
//        strips[i].show();
      }
    }

//   if (received == 't') { /// TESTING
//      strips[2].setPixelColor(3, strips[2].Color(255, 0, 0));
//      strips[2].show();
//    }
}
