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
    def __init__(self,src=0,fps=30,res_wdht='1280x960',verbose=False):
        '''
        Given save location & video properties, start recording w/ a buffer (and add timestamp)
          filepath: desired path to save. must be avi or mp4
          fps: desired frames per second of video. must be integer
          resWdHd: integer tuple of desired resolution

        '''

        self._fps = fps
        self._imwd = int(res_wdht.split('x')[0])
        self._imht = int(res_wdht.split('x')[1])
        self._src = src
        self._imbuf = [] # todo: implement buffer, not just saving directly
        self._cap:cv2.VideoCapture = None
        self._v=verbose

    def opencap(self):
        ''' use to open or reopen a video capture object (for camera) '''
        # todo: if already open, close first
        self._cap = cv2.VideoCapture(self._src)
        self._cap.set(cv2.CAP_PROP_FPS, 1000) # attempt to set highest FPS
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._imwd)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._imht)
        c = self._cap
        c.get(cv2.CAP_PROP_FPS)
        ret, frame = c.read()
        camfps = c.get(cv2.CAP_PROP_FPS)
        if(self._v):print('cam res: {:d} x {:d}'.format(*frame.shape[:2]))
        if(self._v):print('cam fps:', self._fps)
        return True # capture is ready

    def closecap(self):
        self._cap.release()

    def record_n_seconds(self,filepath:str,nseconds:int):
        assert os.path.splitext(filepath)[1] in ['.avi','.mp4'], "invalid format, avi or mp4"
        nmax = float(nseconds)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        res = (
            int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        out = cv2.VideoWriter(filepath, fourcc=fourcc, fps=self._fps, frameSize=res)

        c = self._cap # convenience
        frame:np.ndarray = None
        p = PeriodAuto(1 / self._fps)

        t_el = time.time()
        t0 = time.time()
        ret,frame = c.read()
        out.write(frame)
        n=1
        while(self._cap.isOpened() and nmax > time.time() - t0):
            ret,frame = c.read()
            putText2(frame,tstamp())
            if(time.time()-t_el>=p.per):
                p.update(time.time()-t_el)
                t_el = time.time()
                self._imbuf.append(frame)
                # out.write(frame)
                n+=1
            if(len(self._imbuf)>0):
                out.write(self._imbuf.pop(0))
        t_total = time.time()-t0

        if(len(self._imbuf)>0):
            print('buffer not empty!')
            while(len(self._imbuf)>0):
                out.write(self._imbuf.pop(0))
        out.release()
        if(self._v): print('(fps={:.2f},len={:.2f}): {}'.format(n/t_total,t_total,filepath))
        return True # status that recording is done

def check_video(path):
    vid = cv2.VideoCapture(path)
    nframes = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    frames = []
    success = True
    while(success):
        success,iframe = vid.read()
        frames.append(iframe)
    nframes2=len(frames)
    msg = '{} nFrames={} counted={} imshape={}'.format(
        path, nframes,nframes2,frames[0].shape
    )
    print(msg)
    vid.release()

def choose_video_source():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    print('checking available ports...')
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing.
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
        else:
            is_reading = camera.read()[0]
            if is_reading: working_ports.append(dev_port)
            else: available_ports.append(dev_port)
        dev_port +=1
    print('select desired video source:')
    for i in working_ports: print(i)
    return int(input('video source: '))


if(__name__ == '__main__'):
    import argparse
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # todo: list available sources
    p.add_argument('--fps', default=10, type=int, help='fps')
    p.add_argument('--res', type=str, default="1280x720", help='desired resolution')
    p.add_argument('--rectime', default=5, help='n seconds to record')
    p.add_argument('--srcpick',default=False,action='store_true',
                   help='initialize with choice of sources')
    args = p.parse_args()
    _fps = args.fps
    _res = args.res
    _sec = args.rectime
    srcval = choose_video_source() if(args.srcpick) else 0
    v = VideoCapture(src=srcval,fps=_fps,res_wdht=_res,verbose=True)
    v.opencap()
    v.record_n_seconds('data/out.avi',_sec)
    # v.record_n_seconds('data/out2.avi',_sec) # already know that recording restarts right away
    check_video('data/out.avi')
    # check_video('data/out2.avi')