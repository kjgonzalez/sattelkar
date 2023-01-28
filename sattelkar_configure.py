'''
run this program first to configure correct settings for sattelkar_main.py

todo allow user to provide blank
todo allow user to provide 'd' value
todo add rec_period_s
todo add path_out
'''

import argparse
import os
from common import load_config,save_config
from cap_audio import choose_audio_source
from cap_video import choose_video_source




if(__name__ == '__main__'):
    p=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args=p.parse_args()
    conf:dict = load_config()
    print('\n'*3)
    print('Sattelkar Configuration')
    conf2 = conf.copy()
    print('enter value and press ENTER. leave blank to leave unchanged, enter "d" to reset to default')

    des_audio_src = choose_audio_source()
    des_video_src = choose_video_source()


    des_fps = int(input(f'video fps (integer in range [1,30]) (current:{conf["v_fps"]}):\n> '))
    assert des_fps in range(1,31),'invalid fps value given: '+str(des_fps)

    des_resWH = input(f'video resolution (WxH with aspect ratio 4:3, e.g. 960x720) (current:{conf["v_resWH"]}):\n> ')
    assert 'x' in des_resWH,"invalid expression"
    w,h = des_resWH.split('x')
    assert w.isnumeric() and '.' not in w,"invalid width given"
    assert h.isnumeric() and '.' not in h,"invalid height given"
    assert abs(h/w-0.75)<1e-4 , "invalid aspect ratio"

    # todo rec_period_s

    # todo path_out

    print('old config:',conf)
    conf['a_src'] = des_audio_src
    conf['v_src'] = des_video_src
    conf['v_fps'] = des_fps
    conf['v_resWH']=des_resWH
    save_config(conf)
    print('new configuration:',conf)

# eof
