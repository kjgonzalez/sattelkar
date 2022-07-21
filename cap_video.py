'''
capture video in a buffered manner, to deal with hw / timing limitations
'''

import cv2
import numpy as np
import os
import time

class PeriodAuto:
    '''
    Dynamically fix video framerate. this is a rudimentary PI-controller. A desired period is given,
        and based on the actual time between frames, the period is shortened or lengthened (with a
        rolling average value).
    '''
    def __init__(self,desPer,arrsize=20):
        self.des = desPer
        self.err = np.zeros(arrsize)
        self.ind = 0
        self.errsum=0
    def update(self,val):
        ''' update array of actual periods '''
        e = val-self.des
        self.err[self.ind] = e # error is how much more time than reference was used
        self.errsum += e
        self.ind = self.ind+1 if(self.ind < len(self.err)-1) else 0
    @property
    def correction(self):
        ''' return correction value (to subtract) '''
        return self.err.mean()*2+self.errsum*.2
    @property
    def per(self):
        ''' return actual period value to obtain desired period (on average) '''
        return self.des-self.correction

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

class VideoCapture:
    def __init__(self,filepath:str,fps=30,res_wdht='1280x960',src=0):
        '''
        Given save location & video properties, start recording w/ a buffer (and add timestamp)
          filepath: desired path to save. must be avi or mp4
          fps: desired frames per second of video. must be integer
          resWdHd: integer tuple of desired resolution

        '''
        self.path = filepath
        self.fps = fps
        self.imwd = int(res_wdht.split('x')[0])
        self.imht = int(res_wdht.split('x')[1])
        self.src = src
        self.imbuf = [] # todo: implement buffer, not just saving directly
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FPS,1000)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.imwd)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.imht)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        res = (
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        # todo: set cap properties
        print('des fps:',fps)
        assert os.path.splitext(self.path) in ['.avi','.mp4'], "invalid format, either avi or mp4"
        self.out = cv2.VideoWriter(self.path,fourcc=fourcc,fps=self.fps,frameSize=res)
        c = self.cap
        camfps = c.get(cv2.CAP_PROP_FPS)
        camres = f'{int(c.get(cv2.CAP_PROP_FRAME_WIDTH))} x {int(c.get(cv2.CAP_PROP_FRAME_HEIGHT))}'
        print('cam fps:',camfps)
        print('cam res:',camres)
        camres = f'{int(self.out.get(cv2.CAP_PROP_FRAME_WIDTH))} x {int(self.out.get(cv2.CAP_PROP_FRAME_HEIGHT))}'
        print('vid fps:',self.out.get(cv2.CAP_PROP_FPS))
        print('cam res:',camres)
        # self.cap.release()

    def opencap(self):
        ''' use to open or reopen a video capture object (for camera) '''
        # todo: if already open, close first
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FPS,self.fps)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.imwd)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.imht)
    def record_n_seconds(self,nseconds:int):
        nmax = float(nseconds)

        c = self.cap # convenience
        frame:np.ndarray = None
        p = PeriodAuto(1/self.fps)

        t_el = time.time()
        t0 = time.time()
        ret,frame = c.read()
        self.out.write(frame)
        n=1
        while(self.cap.isOpened() and nmax > time.time()-t0):
            ret,frame = c.read()
            putText2(frame,tstamp())
            if(time.time()-t_el>=p.per):
                p.update(time.time()-t_el)
                t_el = time.time()
                self.out.write(frame)
                n+=1
        t_total = time.time()-t0
        print('frames saved:',n)
        print('t_total:',t_total)
        print('averagefps:',n/t_total)
        c.release()
        self.out.release()

def check_video(path):
    vid = cv2.VideoCapture(path)
    nframes = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    frames = []
    success = True
    while(success):
        success,iframe = vid.read()
        frames.append(iframe)
    nframes2=len(frames)
    print('official nframes:',nframes)
    print('counted  nframes:',nframes2)
    print('imgshape:',frames[0].shape)
    vid.release()



if(__name__ == '__main__'):
    import argparse
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--saveloc', help='where to save video', default='data/vid.avi')
    p.add_argument('--fps', default=10, type=int, help='fps')
    p.add_argument('--res', type=str, default="1280x720", help='desired resolution')
    args = p.parse_args()
    _saveloc = args.saveloc
    _fps = args.fps
    _res = args.res
    print('starting...')
    v = VideoCapture(_saveloc,_fps,_res) # , _fps, _res)
    v.record_n_seconds(10)
    print('done')
    check_video(_saveloc)