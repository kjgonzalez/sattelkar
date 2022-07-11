# Sattelkar Monitor
watch and listen to rockfall events on the sattelkar cirque

## Software objectives
* be able to record video non-stop in 1hr chunks
* record audio non-stop in 1hr chunks
* perhaps combine as single file???
* 

## RPI-Specific Maintenance

### Connect to RPI in the field
todo

### Connect to RPI in office
todo

### Turn on/off various items
#### GUI
note: desktop uses more memory
* `sudo raspi-config` 
* "1 System Options" 
* "S5 Boot / Auto Login"
* choose setting:
    * "B2 Console Autologin" >> console only
    * "B4 Desktop Autologin" >> GUI (desktop)

#### Bluetooth
* disable: `sudo rfkill block bluetooth`
* enable: `sudo rfkill unblock bluetooth`

#### LED
* `sudo vim /boot/config.txt`
* choose setting:
    * enable: comment out the following lines (add "#" before each)
    * disable: uncomment following lines
```
dtparam=act_led_trigger=none
dtparam=act_led_activelow=off
dtparam=pwr_led_trigger=none
dtparam=pwr_led_activelow=off
```

#### HDMI
todo


### Installation
* Raspberry Pi:
    1. `python -m venv ve_sattelkar`
    1. `. ve_sattelkar/bin/activate`
    2. `python -m pip install -r reqs.txt`
    3. `sudo apt-get install portaudio19-dev -y`
    4. `sudo apt-get install python3-dev -y`
    5. `pip install pyaudio opencv-python`
* WINDOWS (Powershell):
    1. `python -m venv ve_sattelkar`
    1. `.\ve_sattelkar\Scripts\activate.ps1` (or *.bat if using CMD)
    2. `python -m pip install -r reqs.txt`
    3. `pip install pipwin`
    4. `pipwin install pyaudio`
    5. `pip install opencv-python`
