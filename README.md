# Sattelkar Monitor
watch and listen to rockfall events on the sattelkar cirque

## Software objectives
* be able to record video non-stop in 1hr chunks
* record audio non-stop in 1hr chunks
* perhaps combine as single file???
* 

## Recommended Settings
### Video 
* option1: res=960x720, fps=30
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

#### Real-Time Clock vs "Fake HW Clock"
The goal of the fake hw clock is to emulate an rtc on the inexpensive rpi. However, the two cannot run together, and thus only one can run at a time.

**Deactivate Software Clock & Activate RTC:**
* Provide commands: 
    ```
    sudo apt-get -y remove fake-hwclock
    sudo update-rc.d -f fake-hwclock remove`
    sudo systemctl disable fake-hwclock`
    ```
* `sudo vim /lib/udev/hwclock-set`: Disable following (add '#'):
    ```
    # if [ -e /run/systemd/system ] ; then
    #   exit 0
    # fi
    ```
* If needed, sync time with current internet time (DO NOT DO WITHOUT INTERNET CONNECTION, WILL GET WRONG VALUE): `sudo hwclock -w`
* Confirm all values good: 
   * `date` >> internet / pi time,
   * `sudo hwclock -r` >> rtc time
source: https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time

**Deactivate RTC and turn on HW clock:**

(todo)


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

### Initial Setup of RPI
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install vim screen

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
