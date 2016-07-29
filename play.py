#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from time import sleep
import RPi.GPIO as GPIO

PLAY = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(PLAY, GPIO.IN)
	
def main():
    timebuttonisstillpressed = 0

    while True:
        if GPIO.input(PLAY) == True:
            if timebuttonisstillpressed == 0:
                print("Play. Yes!")
                subprocess.Popen(['mpg123', 'music/01.mp3'])
        
            elif timebuttonisstillpressed > 2:
                subprocess.call(['killall', 'mpg123'])
                print("Stop.")
                timebuttonisstillpressed = 0
            timebuttonisstillpressed = timebuttonisstillpressed + 0.1
        else:
            timebuttonisstillpressed = 0

        sleep(0.2);

if __name__ == "__main__":
    try:
        print ("Taster drücken, um Ton abzuspielen, CTRL+C beendet das Programm.")
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
