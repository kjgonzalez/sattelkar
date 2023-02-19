#!/usr/bin/env bash
# automatically unmount (if mounted), fsck, and remount hdd5tb
sudo mount /media/pi/hdd5tb
sudo fsck /dev/sda1 -y
sudo mount /dev/sda1 /media/pi/hdd5tb


# eof

