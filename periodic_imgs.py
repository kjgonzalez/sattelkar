'''
record images for two different purposes:
* low-frequency, high-resolution stream
* high-frequency, low-resolution

ITEM DESCRIP
nope auto-scale timestamp
done fn: take raw image and resize, apply timestamp
done record images at given rates / qualities
done control user input: max fps, etc
done: check that user didn't give non-integer period

'''

import numpy as np
import cv2
import time
import argparse
from copy import deepcopy
import os

def showimg(im,windowtitle='Press "q" to exit'):
    cv2.imshow(windowtitle,im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def tstamp(withms=True):
    # todo: figure out if should use utc -> yes
    _t = time.time()
    ms = str(round(_t-int(_t),3))[1:]
    ms = '{:0<4}'.format(ms) # add 0's until have 3 digits + '.'
    base = time.strftime('%Y%m%d_%H%M%S',time.localtime(_t))
    return (base+ms) if(withms) else (base)

def putText2(im:np.ndarray, _txt:str, origin:tuple=None):
    '''
    Custom putText function. default is white-on-black, upper-left corner, 13px font

    im: cv2 image. modification done in-place
    _txt: text to display
    origin: bottom-left pixel location, (x,y) location. default is top-left of image
    '''
    ht_font_base = 22
    ht_font = 13
    font=cv2.QT_FONT_NORMAL
    if(origin is None): origin = (1,ht_font+2)
    txtht=ht_font/ht_font_base
    cv2.putText(im, _txt, origin, font, txtht, (0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(im, _txt, origin, font, txtht, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)


def resize2(im,_ratio):
    return cv2.resize(im, None, fx=_ratio, fy=_ratio)

def saveFrame(im,img_ratio,loc):
    img = deepcopy(im)
    if(img_ratio != 1.0):
        img = resize2(img,img_ratio)
    putText2(img,tstamp())
    cv2.imwrite(loc,img)

if(__name__ == '__main__'):
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--src',default=0, help='video source')
    p.add_argument('--per0',default=3600, help='high quality capture period')
    p.add_argument('--per1',default=1, help='low quality capture period')
    p.add_argument('--res1',default=400, help='resolution1, low quality img width')
    p.add_argument('--vis',default=False,action='store_true',help='show video feed')
    p.add_argument('--path0',default='img_hidef',help='high quality capture path')
    p.add_argument('--path1',default='img_lodef',help='low quality capture path')
    p.add_argument('--verbose',default=False,action='store_true',help='print to console')
    args = p.parse_args()

    SRC = int(args.src)
    PER0 = int(args.per0)
    PATH0 = args.path0
    PATH1 = args.path1
    PER1 = int(args.per1)
    RES1 = int(args.res1)
    VIS = bool(args.vis)
    VERB = bool(args.verbose)
    assert PER0>0, f"invalid period0 given: {args.per0}"
    assert PER1>0, f"invalid period1 given: {args.per1}"


    # initialize
    cap = cv2.VideoCapture(SRC)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # _resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    if(not os.path.exists(PATH0)): os.makedirs(PATH0)
    if(not os.path.exists(PATH1)): os.makedirs(PATH1)
    print(f'high quality path: {os.path.abspath(PATH0)}')
    print(f'low quality path:  {os.path.abspath(PATH1)}')
    print('program running...')

    t0=time.time()-(PER0+1) # ensure that an image is saved at very start of program
    t1=time.time()-(PER1+1)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if(time.time()-t0 >= PER0):
            t0=time.time()
            txt = tstamp()
            if(VERB): print(txt,'lodef img saved')
            saveFrame(frame,1.0,f'{PATH0}/{txt}.jpg')
        if(time.time()-t1 >= PER1):
            t1=time.time()
            txt = tstamp()
            if(VERB): print(txt,'hidef img saved')
            ratio = RES1/frame.shape[1] # shape = (ht,wd,channels)
            saveFrame(frame,ratio,f'{PATH1}/{txt}.jpg')
        if(VIS):
            cv2.imshow('frame', frame)
            if(cv2.waitKey(1) & 0xFF == ord('q')):
                break

# eof
