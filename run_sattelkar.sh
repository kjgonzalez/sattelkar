#!/usr/bin/env bash
# Run Sattelkar Monitor Program with configured settings
screen -d -S sattelkar -m /home/pi/sattelkar/ve_sattelkar/bin/python /home/pi/sattelkar/sattelkar_main.py
echo "new screen started. type 'screen -ls' to view available screeens"
