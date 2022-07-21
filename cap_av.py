'''
use multiprocessing to capture both audio and video at the same time
'''

import multiprocessing as mp
import time
from cap_audio import AudioCapture
from cap_video import VideoCapture, tstamp



class AVCap:
    def __init__(self,vidsrc,audiosrc,folderpath:str):
        '''
        todo: avoid overwriting previous files
        todo: create two processes to capture everything
        todo: create function to combine things (perhaps linux-specific?)

        '''
        pass
    def record_n_seconds(self,nseconds:int):
        ''' create two processes to capture audio and video at the same time'''
        pass

if(__name__ == '__main__'):
    print('hello')

