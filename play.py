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
CONNECTION_ID = {'host':HOST, 'port':PORT}

# Configure IO ports
PLAY01 = 25
PLAY02 = 24
PLAY03 = 23
CHANNEL_LIST = [PLAY01, PLAY02, PLAY03]

def main():
    print ("Taste drücken, um Song abzuspielen, CTRL+C beendet das Programm.")

    initGPIO()
    client = MPDClient()
    establishConnectionToMpdServer(client, CONNECTION_ID)
    updateAndLoadLatestsPlaylist(client)
    stopPlaybackAfterCurrentSong(client)

    while True:
        if GPIO.input(PLAY01) == True:
            handleButtonClick(client, '0')
        if GPIO.input(PLAY02) == True:
            handleButtonClick(client, '1')
        if GPIO.input(PLAY03) == True:
            handleButtonClick(client, '2')

        sleep(0.1);


def initGPIO():
    print("Initializing GPIO pins ...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHANNEL_LIST, GPIO.IN)


def establishConnectionToMpdServer(client, connection_id):
    try:
        client.connect(**connection_id)
    except SocketError:
        return False
    return True


def updateAndLoadLatestsPlaylist(client):
    print('Loading playlist ...')
    client.update()
    client.clear()
    os.system("mpc ls | mpc add")
    print client.playlist()
    print('--------------------')


def stopPlaybackAfterCurrentSong(client):
    client.single(1)


def handleButtonClick(client, song):
    if (client.status()["state"] == "play" or client.status()["state"] == "pause"):
        if client.currentsong()["pos"] != song:
            print("not the same")
            client.stop()

    if client.status()["state"] == "stop":
        client.play(song)
        print client.currentsong()
    else:
        client.pause()
        print client.status()["state"]


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
