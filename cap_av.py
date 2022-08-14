'''
use multiprocessing to capture both audio and video at the same time

STAT-DESCRIPTION
todo be able to choose source directly from AVCap
todo record for a certain amount of seconds
todo create N recordings with a simple forloop
todo be able to splice together audio and video through ffmpeg (?)
todo a function or class that can record N seconds of data at a time
'''

import multiprocessing as mp
import time
import os
from cap_audio import AudioCapture
from cap_video import VideoCapture, tstamp

def rec_audio(q_:mp.Queue,pathbase:str,duration:int,opencap):
    a = AudioCapture()
    q_.put(a.opencap())

    print('aud, current q len:',q_.qsize())
    while(q_.qsize()<2):
        time.sleep(0.001) # wait a few seconds for sync
    print('AUD STARTING')
    a.record_n_seconds(pathbase+'.wav',duration)
    q_.get() # remove object from queue
    print('audio done')

def rec_video(q_:mp.Queue,pathbase:str,duration:int,opencap):
    v = VideoCapture()
    q_.put(v.opencap())
    print('vid, current q len:',q_.qsize())
    while(q_.qsize()<2):
        time.sleep(0.001) # wait a few seconds for sync
    print('VID STARTING')
    v.record_n_seconds(pathbase+'.avi',duration)
    q_.get() # remove object from queue
    print('vid, current q len:',q_.qsize())
    print('audio done')


if(__name__ == '__main__'):

    pathfolder = 'data/'
    basename = os.path.abspath(os.path.join(pathfolder,tstamp(False)))

    queue = mp.Queue()
    # using this to sync things means that the arguments aren't copied, only
    #   the objects. as long as you don't access to devices, you should be fine.
    # todo: pass each capture object, already open, to record audio/video
    pa = mp.Process(target=rec_audio,args=(queue,basename,5))
    pv = mp.Process(target=rec_video,args=(queue,basename,5))

    print('starting...')
    pv.start()
    pa.start()

    pv.join()
    pa.join()
    print('done')


    # av = AVCap('data/',debug=True)
    # av.record_n_seconds(10)






