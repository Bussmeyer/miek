#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import os

from time import sleep
from mpd import (MPDClient)
from contextlib import contextmanager


# Configure MPD connection settings
HOST = 'localhost'
PORT = '6600'
client = MPDClient()

# Configure IO ports
PLAY01 = 25
PLAY02 = 24
PLAY03 = 23
CHANNEL_LIST = [PLAY01, PLAY02, PLAY03]


def main():
    print ("Taste drücken, um Song abzuspielen, CTRL+C beendet das Programm.")
    initGPIO()
    updateAndLoadLatestsPlaylist()
    stopPlaybackAfterCurrentSong()
    andNowWaitForButtonClicksAndHandleThem()


def initGPIO():
    print("Initializing GPIO pins ...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHANNEL_LIST, GPIO.IN)


@contextmanager
def connectionToMpdServer():
    try:
        client.connect(HOST, PORT)
        yield
    finally:
        client.close()
        client.disconnect()


def updateAndLoadLatestsPlaylist():
    with connectionToMpdServer():
        print('Loading playlist ...')
        client.update()
        client.clear()
        os.system("mpc ls | mpc add")
        print client.playlist()
        print('--------------------')


def stopPlaybackAfterCurrentSong():
    with connectionToMpdServer():
        client.single(1)


def andNowWaitForButtonClicksAndHandleThem():
    while True:
        if GPIO.input(PLAY01) == True:
            handleButtonClick(client, '0')
        if GPIO.input(PLAY02) == True:
            handleButtonClick(client, '1')
        if GPIO.input(PLAY03) == True:
            handleButtonClick(client, '2')

        sleep(0.1);


def handleButtonClick(client, song):
    with connectionToMpdServer():
        status = client.status()["state"]
        currentsong = client.currentsong()["pos"]

        if (status == "play" or status == "pause"):
            if currentsong == song:
                client.pause()
            elif currentsong != song:
                client.stop()
                client.play(song)
        elif status == "stop":
            client.play(song)
        else:
            print("Error")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit
