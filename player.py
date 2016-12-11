#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import os

from time import sleep
from mpd import (MPDClient)
from contextlib import contextmanager


class player:

    def __init__(self, channelList):
        print ("Taste drücken, um Song abzuspielen, CTRL+C beendet das Programm.")
        self.client = MPDClient()
        # Configure MPD connection settings
        self.host = 'localhost'
        self.port = '6600'
        self.initGPIO(channelList)
        self.updateAndLoadLatestsPlaylist()
        self.stopPlaybackAfterCurrentSong()
        self.andNowWaitForButtonClicksAndHandleThem()

    def initGPIO(channelList):
        print("Initializing GPIO pins ...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channelList, GPIO.IN)

    @contextmanager
    def connectionToMpdServer(self):
        try:
            self.client.connect(self.host, self.port)
            yield
        finally:
            self.client.close()
            self.client.disconnect()

    def updateAndLoadLatestsPlaylist(self):
        with self.connectionToMpdServer():
            print('Loading playlist ...')
            self.client.update()
            self.client.clear()
            os.system("mpc ls | mpc add")
            print self.client.playlist()
            print('--------------------')

    def stopPlaybackAfterCurrentSong(self):
        with self.connectionToMpdServer():
            self.client.single(1)

    def andNowWaitForButtonClicksAndHandleThem(self):
        while True:
            if GPIO.input(PLAY01) == True:
                self.handleButtonClick(self.client, '0')
            if GPIO.input(PLAY02) == True:
                self.handleButtonClick(self.client, '1')
            if GPIO.input(PLAY03) == True:
                self.handleButtonClick(self.client, '2')

            sleep(0.1);

    def handleButtonClick(self, client, song):
        with self.connectionToMpdServer():
            status = self.client.status()["state"]

            if (status == "play" or status == "pause"):
                if self.client.currentsong()["pos"] == song:
                    self.client.pause()
                elif self.client.currentsong()["pos"] != song:
                    self.client.stop()
                    self.client.play(song)
            elif status == "stop":
                self.client.play(song)
            else:
                print("Error")


if __name__ == "__main__":
    # Configure IO ports
    PLAY01 = 25
    PLAY02 = 24
    PLAY03 = 23
    CHANNEL_LIST = [PLAY01, PLAY02, PLAY03]

    try:
        player = player(CHANNEL_LIST)
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit
