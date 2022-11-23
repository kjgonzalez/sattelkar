'''
record camera at default settings for a few seconds
'''

import cv2
import time
import numpy as np

_src = 0
_tmax = float(5) # small correction for camera delay... ?
_fpath = 'data/hello_video.avi'

cap = cv2.VideoCapture(_src)
_fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)


fourcc = cv2.VideoWriter_fourcc(*'XVID')
_resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

out = cv2.VideoWriter(_fpath, fourcc=fourcc, fps=_fps, frameSize=_resolution)

print('starting...')
t0 = time.time()
nframes=0
nmax = _fps*_tmax
# while(t0+5 >= time.time() and cap.isOpened()):
while(nmax>nframes and cap.isOpened()):
    ret, frame = cap.read()
    out.write(frame)
    nframes+=1
print('elapsed time:',time.time()-t0)
print('nframes:',nframes)
print('done')
