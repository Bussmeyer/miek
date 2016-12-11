#include "Arduino.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

// Constants
const int rxPinOnTheArduino = 10;
const int txPinOnTheArduino = 11;
const int baudRate          = 115200;
const int myBaudRate        = 9600; // initialize serial communication at 'baudRate' bits per second
const int volume            = 5;     //Set volume value. From 0 to 30
const int activated         = LOW;
const int buttonPlaylist01  = 2;      // the number of the pushbutton pin
const int buttonPlaylist02  = 3;      // the number of the pushbutton pin

// Variables
int buttonStatePlaylist01   = 0;      // variable for reading the pushbutton status
int buttonStatePlaylist02   = 0;

SoftwareSerial mySoftwareSerial(rxPinOnTheArduino, txPinOnTheArduino); // RX, TX
DFRobotDFPlayerMini myDFPlayer;
void printDetail(uint8_t type, int value);

// Functions
void setup()
{
  pinMode(buttonPlaylist01, INPUT_PULLUP);
  pinMode(buttonPlaylist02, INPUT_PULLUP);
  
  mySoftwareSerial.begin(9600);
  Serial.begin(baudRate);

//  myDFPlayer.volume(volume);
//  myDFPlayer.play(1);  //Play the first mp3
//  myDFPlayer.playFolder(1, 1);
//  myDFPlayer.playFolder(15, 4);  //play specific mp3 in SD:/15/004.mp3; Folder Name(1~99); File Name(1~255)
//  myDFPlayer.playLargeFolder(2, 999); //play specific mp3 in SD:/02/004.mp3; Folder Name(1~10); File Name(1~1000)
//  myDFPlayer.loopFolder(1); //loop all mp3 files in folder SD:/05.



  

  Serial.println();
  Serial.println(F("DFRobot DFPlayer Mini Demo"));
  Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));
  
  if (!myDFPlayer.begin(mySoftwareSerial)) {  //Use softwareSerial to communicate with mp3.
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1.Please recheck the connection!"));
    Serial.println(F("2.Please insert the SD card!"));
    while(true);
  }
  Serial.println(F("DFPlayer Mini online."));
  
  myDFPlayer.volume(10);  //Set volume value. From 0 to 30
  myDFPlayer.play(1);  //Play the first mp3
}

void loop()
{
  if  (digitalRead(buttonPlaylist01) == activated) {
    Serial.println("Button 01 pressed");
  }

  if  (digitalRead(buttonPlaylist02) == activated) {
    Serial.println("Button 02 pressed");
  }

  
  static unsigned long timer = millis();
  if (millis() - timer > 3000) {
    timer = millis();
    myDFPlayer.next();  //Play next mp3 every 3 second.
  }
  
  if (myDFPlayer.available()) {
    printDetail(myDFPlayer.readType(), myDFPlayer.read()); //Print the detail message from DFPlayer to handle different errors and states.
  }
}

void printDetail(uint8_t type, int value){
  switch (type) {
    case TimeOut:
      Serial.println(F("Time Out!"));
      break;
    case WrongStack:
      Serial.println(F("Stack Wrong!"));
      break;
    case DFPlayerCardInserted:
      Serial.println(F("Card Inserted!"));
      break;
    case DFPlayerCardRemoved:
      Serial.println(F("Card Removed!"));
      break;
    case DFPlayerCardOnline:
      Serial.println(F("Card Online!"));
      break;
    case DFPlayerPlayFinished:
      Serial.print(F("Number:"));
      Serial.print(value);
      Serial.println(F(" Play Finished!"));
      break;
    case DFPlayerError:
      Serial.print(F("DFPlayerError:"));
      switch (value) {
        case Busy:
          Serial.println(F("Card not found"));
          break;
        case Sleeping:
          Serial.println(F("Sleeping"));
          break;
        case SerialWrongStack:
          Serial.println(F("Get Wrong Stack"));
          break;
        case CheckSumNotMatch:
          Serial.println(F("Check Sum Not Match"));
          break;
        case FileIndexOut:
          Serial.println(F("File Index Out of Bound"));
          break;
        case FileMismatch:
          Serial.println(F("Cannot Find File"));
          break;
        case Advertise:
          Serial.println(F("In Advertise"));
          break;
        default:
          break;
      }
      break;
    default:
      break;
  }

}

