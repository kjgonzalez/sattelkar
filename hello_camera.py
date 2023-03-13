''' basic webcam-like functionality, just show a preview window of what is seen '''

import argparse
import cv2
import time

def putText2(im, _txt:str, origin:tuple=None):
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

class RunningAverage:
    def __init__(self,size=10):
        self.vals=[0 for i in range(size)]
        self.max = size
        self.ind=0
    def update(self,value):
        self.vals[self.ind]=value
        self.ind+=1
        if(self.ind>=self.max):
            self.ind = 0
    def avgval(self,rounding=3):
        return round(sum(self.vals)/self.max,rounding)

if(__name__ == '__main__'):
    p=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--src',default=0,type=int,help='Camera source')
    args=p.parse_args()

    src = args.src
    avgprint = True
    cap = cv2.VideoCapture(src)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    
    print('press "q" to exit')
    t0 = time.time()
    ra = RunningAverage()
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if(avgprint):
            meanbgr = frame.mean(0).mean(0).astype(int)
            ra.update(time.time()-t0)
            t0 = time.time()
            putText2(frame,f'fps:{1/ra.avgval(8):0.2f}  avgcolor:{meanbgr}')
            # print average color of frame
            # print('mean BGR value:',frame.mean(0).mean(0).astype(int))
    
        # Display the resulting frame
        cv2.imshow('frame',frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
# eof

