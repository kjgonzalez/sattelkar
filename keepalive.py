'''
simple method to keep hdd alive 
'''
import time
from common import tstamp
path = '/media/pi/hdd5tb/keepalive.txt'


if(__name__=='__main__'):
    while(True):
        with open(path,'a') as f:
            f.write(str(tstamp())+'\n')
        print(tstamp())
        time.sleep(30)
# eof

