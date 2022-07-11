'''
compare various framerates
'''

import cv2
import time
import argparse
import numpy as np

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
    im2 = im.copy()
    cv2.putText(im2, _txt, origin, font, txtht, (0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(im2, _txt, origin, font, txtht, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
    return im2



def showimg(im,windowtitle='Press "q" to exit'):
    cv2.imshow(windowtitle,im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class Lap:
    def __init__(self,avg=1):
        self.t0=time.time()
        self.avg=avg
        self.vals=[0 for i in range(avg)]
        self.p:int=0
    def tik(self):
        self.vals[self.p] = time.time()-self.t0
        self.t0=time.time()
        self.p = self.p+1 if(self.p+1<self.avg) else 0
        return self.getval()
    def getval(self):
        if(self.avg==1): return self.vals[0]
        k = [i for i in self.vals if(i!=0)]
        if(len(k)==0): return 0
        return np.mean(k)



if(__name__ == '__main__'):
    # p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # p.add_argument('--verbose',default=False,action='store_true',help='print to console')
    # args = p.parse_args()

    # FP's to try out: 30,15,10,5



    # initialize
    cap = cv2.VideoCapture(0)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # _resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(cap.get(cv2.CAP_PROP_FPS))
    ctr=0
    t30=time.time()
    s30 = Lap(50)
    s15 = Lap(25)
    s10 = Lap(15)
    s5 = Lap(5)
    while(cap.isOpened()):
        ret, frame = cap.read()
        # 30 fps
        if((ctr % (30 / 30)) == 0): cv2.imshow('f1', putText2(frame, str(round(1 / s30.tik(), 3))))
        if((ctr % (30 / 15)) == 0): cv2.imshow('f2', putText2(frame, str(round(1 / s15.tik(), 3))))
        if((ctr % (30 / 10)) == 0): cv2.imshow('f3', putText2(frame, str(round(1 / s10.tik(), 3))))
        if((ctr % (30 / 5)) == 0): cv2.imshow('f4', putText2(frame, str(round(1 / s5.tik(), 3))))

        ctr+=1
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()
