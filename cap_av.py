'''
use multiprocessing to capture both audio and video at the same time

STAT-DESCRIPTION
nope be able to choose source directly from CapAV - should be done in "selector", which saves to config
done record for a certain amount of seconds
nope: pass each capture object, already open, to record audio/videotodo creater "SourceSelector.py", allowing user to first go through config
done be able to record 5s video
done be able to record 5s audio
done be able to record audio & video at the same time
done a function or class that can record N seconds of data at a time
todo create N recordings with forloop
todo be able to splice together audio and video through ffmpeg (?)

missing:

note: general command for ffmpeg follows:
ffmpeg -i VIDEO.avi -i AUDIO.wav -c:v copy -c:a aac ../OUTFILE.mp4
'''

import multiprocessing as mp
import time
import os
from cap_audio import CaptureAudio
from cap_video import CaptureVideo, tstamp

def _rec_audio(q_:mp.Queue,pathfile:str,duration:int,src:int,verbose=False):
    ''' REQUIRED full function for audio thread '''
    a = CaptureAudio(src=src)
    q_.put(a.opencap())
    # print('aud, current q len:',q_.qsize())
    if(verbose): print('audio ready')
    while(q_.qsize()<2):
        time.sleep(0.001) # wait a few seconds for sync
    if(verbose): print('AUD STARTING')
    a.record_n_seconds(pathfile,duration) # user must give file extension
    q_.get() # remove object from queue
    # print('audio done')

def _rec_video(q_:mp.Queue,pathfile:str,duration:int,src:int,fps:int,resWH:str,verbose=False):
    ''' REQUIRED full function for video thread'''
    v = CaptureVideo(src=src, fps=fps, resWH=resWH)
    q_.put(v.opencap())
    # print('vid, current q len:',q_.qsize())
    if(verbose): print('video ready')
    while(q_.qsize()<2):
        time.sleep(0.001) # wait a few seconds for sync
    if(verbose): print('VID STARTING')
    v.record_n_seconds(pathfile,duration) # user must give file extension
    q_.get() # remove object from queue
    # print('vid, current q len:',q_.qsize())
    # print('video done')

def record_n_seconds(path_folder,duration_s,
                     a_src=2,v_src=0,v_fps=30,v_resWH='960x720'):
    '''
    Abstracted recording function. Handles both audio and video, given the basic sources and settings. Automatically
      combines audio and video streams into single file. Inserts formatted timestamp into video. Output file name is
      based on starting time of recording (not including delay of stream start)

    todo: name recording based on exact moment recording actually started
    '''
    queue = mp.Queue()
    # using this to sync things means that the arguments aren't copied, only
    #   the objects. as long as you don't access to devices, you should be fine.
    #
    istamp = tstamp(withms=False)
    fpath_a = os.path.join(path_folder,f'{istamp}temp.wav')
    fpath_v = os.path.join(path_folder,f'{istamp}temp.avi')
    fpath_av = os.path.join(path_folder,f'{istamp}.avi')
    # fpath_v = path_folder+'temp.avi'
    # fpath_av = path_folder+f'{tstamp(withms=False)}.avi'
    pa = mp.Process(target=_rec_audio,args=(queue,fpath_a,duration_s,a_src))
    pv = mp.Process(target=_rec_video,args=(queue,fpath_v,duration_s,v_src,v_fps,v_resWH))

    pv.start() # initialize queues
    pa.start()
    pv.join() # when complete, join queues and unify two processes
    pa.join()

    # combine audio/video into single file, remove individual parts
    os.system('ffmpeg -i {} -i {} -c:v copy -c:a aac {} {}'.format(
        fpath_v,fpath_a,fpath_av,
        '>/dev/null 2>&1' # warning / error message suppression
    ))
    os.remove(fpath_v)
    os.remove(fpath_a)
    print('done:',fpath_av)

'''
idea: have them capture for specified time, then wait until both ready, then start 
'''





if(__name__ == '__main__'):
    folderpath = 'data/'
    record_n_seconds(folderpath,5,2,0,30,'960x720')







