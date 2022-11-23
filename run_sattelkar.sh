#!/usr/bin/env bash
# Run Sattelkar Monitor Program with configured settings
screen -d -S sattelkar -m /home/pi/sattelkar/ve_sattelkar/bin/python /home/pi/sattelkar/main.py
echo "new screen successfully started. type 'screen -ls' to view available screeens"
