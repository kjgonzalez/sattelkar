#!/usr/bin/env bash
# Run Sattelkar Monitor Program with configured settings. This file 
#   automatically starts on reboot via cron (run "crontab -e" to edit). If the 
#   auto-start of sattelkar should be disabled, create a file called "norun" 
#   in the home directory (run "touch ~/norun"). to reenable auto-start, delete
#   the file.

#screen -d -S sattelkar -m /home/pi/sattelkar/ve_sattelkar/bin/python /home/pi/sattelkar/sattelkar_main.py
pathrestarts=/media/pi/hdd5tb/restarts.txt
date >> "$pathrestarts" # track each time rpi is restarted
if test -f ~/norun; then
  echo "autorun disabled" >> "$pathrestarts"
else
  # reset proper config to allow screen to work with cron (schedule manager)
  chmod 700 ~/.screen
  export SCREENDIR=/home/pi/.screen
  /usr/bin/screen -d -S test -m watch -n 5 "df -h"
fi

# eof

