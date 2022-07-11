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


### Turn on/off various items
#### GUI
`sudo raspi-config` >> "1 System Options" >> "S5 Boot / Auto Login"
* "B2 Console Autologin" >> console only
* "B4 Desktop Autologin" >> GUI (desktop)
note: desktop uses more memory

#### Bluetooth
disable: `sudo rfkill block bluetooth`
enable: `sudo rfkill unblock bluetooth`

#### LED
`sudo vim /boot/config.txt`
enable: comment out the following lines (add "#" before each)
disable: uncomment following lines
```
dtparam=act_led_trigger=none
dtparam=act_led_activelow=off
dtparam=pwr_led_trigger=none
dtparam=pwr_led_activelow=off
```

#### HDMI
todo


### Installation
1. `python -m venv ve_sattelkar`
2. (activate env)
3. `python -m pip install -r reqs.txt`
4. `python -m pip install <path to wheel>`
5. ???
6. LINUX: install pyaudio
    1. sudo apt-get install portaudio19-dev
    2. sudo apt-get install python3-dev
    3. pip install pyaudio
7. WINDOWS: install pyaudio
    1. pip install pipwin
    2. pipwin install pyaudio

WINDOWS, opencv: 
    1. python -m pip install opencv-python
RASPBERRYPI, opencv: 
    1. python -m pip install opencv-python 
