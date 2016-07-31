#!/bin/bash

sudo apt-get update -y
sudo apt-get install -y alsa-utils mpg123 mpd mpc python-dev python-rpi.gpio python-mpd python-pyudev

ln -s /var/lib/mpd/music ~/music

sudo modprobe snd_bcm2835
sudo amixer cset numid=3 1

sudo mv ~/miek/configs/startupsound /etc/init.d/
sudo chown root: /etc/init.d/startupsound
sudo chmod 755 /etc/init.d/startupsound
sudo update-rc.d startupsound defaults


echo "Preparing for reboot ..."
echo "If you're using SSH, you'll have to reconnect after it boots."
sleep 2
sudo reboot
