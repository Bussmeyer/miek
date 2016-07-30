#!/bin/bash

sudo apt-get update -y
sudo apt-get install -y alsa-utils mpg123 mpd mpc python-dev python-rpi.gpio python-mpd python-pyudev

sudo modprobe snd_bcm2835
sudo amixer cset numid=3 1

echo "Preparing for reboot ..."
echo "If you're using SSH, you'll have to reconnect after it boots."
sleep 2
sudo reboot
