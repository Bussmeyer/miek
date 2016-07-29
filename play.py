#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)

print ("Taster drücken, um Ton abzuspielen, CTRL+C beendet das Programm.")

try:
    while True:
        if (GPIO.input(25) == True):
            print("Gedrückt. Yes!")
            os.system('mpg123 -q tests/1000Hz-5sec.mp3 &')
        sleep(0.1);
except KeyboardInterrupt:
    GPIO.cleanup()
