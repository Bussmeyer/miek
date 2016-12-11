#include "Arduino.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

// Constants
const int rxPinOnTheArduino = 10;
const int txPinOnTheArduino = 11;
const int volume            = 2;      //Set volume value. From 0 to 30
const int activated         = LOW;
const int buttonPlaylist1  = 2;      // the number of the pushbutton pin
const int buttonPlaylist2  = 3;      // the number of the pushbutton pin


SoftwareSerial mySoftwareSerial(rxPinOnTheArduino, txPinOnTheArduino); // RX, TX
DFRobotDFPlayerMini myDFPlayer;

int currentFolder = 1;
int currentSong = 1;
void printDetail(uint8_t type, int value);



// Functions
void setup()
{
  pinMode(buttonPlaylist1, INPUT_PULLUP);
  pinMode(buttonPlaylist2, INPUT_PULLUP);

  mySoftwareSerial.begin(9600);
  Serial.begin(115200);
  
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

  myDFPlayer.setTimeOut(500); //Set serial communictaion time out 500ms
  myDFPlayer.volume(volume);  //Set volume value. From 0 to 30




  // Check all the different folders
  int songs1 = myDFPlayer.readFileCountsInFolder(1);
  int songs2 = myDFPlayer.readFileCountsInFolder(2);
  int songs3 = myDFPlayer.readFileCountsInFolder(3);

  Serial.print(F("Songs in folder 01: "));
  Serial.println(songs1);
  Serial.print(F("Songs in folder 02: "));
  Serial.println(songs2);
  Serial.print(F("Songs in folder 03: "));
  Serial.println(songs3);

  
}

void loop()
{

  if  (digitalRead(buttonPlaylist1) == activated) {
    currentFolder = 1;
    myDFPlayer.playLargeFolder(currentFolder, 1);
    Serial.println("Button 01 pressed");
    Serial.println(myDFPlayer.readCurrentFileNumber());
  }

  if  (digitalRead(buttonPlaylist2) == activated) {
    Serial.println("Button 02 pressed");
    currentFolder = 2;
    myDFPlayer.playLargeFolder(currentFolder, 1);
    Serial.println(myDFPlayer.readCurrentFileNumber());
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

