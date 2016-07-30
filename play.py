#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from time import sleep
import RPi.GPIO as GPIO

from mpd import (MPDClient, CommandError)
from socket import error as SocketError
from time import sleep

PREVIOUS = 25
PLAY = 24
NEXT = 23
LIBRARY = 'music/'

isPlaying = False

def main():
    initGPIO()
    print ("Starting player ...")
    print ("Taste drücken, um Ton abzuspielen, CTRL+C beendet das Programm.")

    while True:
        if GPIO.input(PLAY) == True:
            if isPlaying == True:
                stop()
            elif isPlaying == False:
                play('tests/440Hz-5sec.mp3')

        sleep(0.1);

def initGPIO():
    print("Initializing GPIO pins ...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PREVIOUS, GPIO.IN)
    GPIO.setup(PLAY, GPIO.IN)
    GPIO.setup(NEXT, GPIO.IN)

def play(song):
    global isPlaying

    subprocess.Popen(['mpg123', '-q', song])
    isPlaying = True
    print("Play")

def stop():
    global isPlaying

    subprocess.call(['killall', 'mpg123'])
    isPlaying = False
    print("Stop")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
