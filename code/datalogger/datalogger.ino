/*
  SD card datalogger

  This example shows how to log data from three analog sensors
  to an SD card using the SD library. Pin numbers reflect the default
  SPI pins for Uno and Nano models

  The circuit:
   analog sensors on analog pins 0, 1, and 2
   SD card attached to SPI bus as follows:
 ** SDO - pin 11
 ** SDI - pin 12
 ** CLK - pin 13
 ** CS - depends on your SD card shield or module.
 		Pin 10 used here for consistency with other Arduino examples
    (for MKR Zero SD: SDCARD_SS_PIN)

  created  24 Nov 2010
  modified  24 July 2020
  by Tom Igoe

  This example code is in the public domain.

*/

#include <SPI.h>
#include <SD.h>

const int chipSelect = 10;
char data[250];
char filename[50];

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  // wait for Serial Monitor to connect. Needed for native USB port boards only:
  while (!Serial);

  Serial.print("Initializing SD card...");

  if (!SD.begin(chipSelect)) {
    Serial.println("initialization failed. Things to check:");
    Serial.println("1. is a card inserted?");
    Serial.println("2. is your wiring correct?");
    Serial.println("3. did you change the chipSelect pin to match your shield or module?");
    Serial.println("Note: press reset button on the board and reopen this Serial Monitor after fixing your issue!");
    while (true);
  }
  Serial.println("initialization done.");
  int i = 0;
  do {
    sprintf(filename,"log%i.txt",i++);
  } while(SD.exists(filename));
  Serial.println(filename);
}

void loop() {
  File dataLog;
  int i = 0;
  // filling buffer
  while(i < 200) {
    while(Serial.available() > 0) {
      data[i] = Serial.read();
      i++;
    }
  }
  
  dataLog = SD.open(filename, FILE_WRITE);
  if (dataLog) {
    dataLog.write(data,200);
    Serial.println("Wrote buffer");
  }
  else {
    Serial.println("error opening datalog.txt");
  }
  dataLog.close();
}
