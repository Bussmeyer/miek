#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import os

from time import sleep
from mpd import (MPDClient, CommandError)
from socket import error as SocketError

# Configure MPD connection settings
HOST = 'localhost'
PORT = '6600'
CON_ID = {'host':HOST, 'port':PORT}

# Configure IO ports
PREVIOUS = 25
PLAY = 24
NEXT = 23

def main():
    initGPIO()

    client = MPDClient()
    mpdConnect(client, CON_ID)
    client.update()
    client.clear()
    os.system("mpc ls | mpc add")
    print client.playlist()

    print ("Starting player ...")
    print ("Taste drücken, um Ton abzuspielen, CTRL+C beendet das Programm.")

    while True:
        if GPIO.input(PLAY) == True:
            if client.status()["state"] == "stop":
                client.play()
                print client.currentsong()
            else:
                client.pause()

        if GPIO.input(PREVIOUS) == True:
            client.previous()
            print client.currentsong()

        if GPIO.input(NEXT) == True:
            client.next()
            print client.currentsong()

        sleep(0.1);

def initGPIO():
    print("Initializing GPIO pins ...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PREVIOUS, GPIO.IN)
    GPIO.setup(PLAY, GPIO.IN)
    GPIO.setup(NEXT, GPIO.IN)

def mpdConnect(client, con_id):
    """
    Simple wrapper to connect MPD.
    """
    try:
            client.connect(**con_id)
    except SocketError:
            return False
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
