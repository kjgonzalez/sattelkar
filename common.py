'''
basic utility functions common to multiple modules
'''

import time
import json
import os
osp = os.path
req_vals = 'a_src v_src v_fps v_resWH rec_period_s path_out'.split(' ')
default_vals = [2,0,20,'960x720',3600,'/media/pi/hdd5tb/data_sattelkar'] # todo make default values

def tstamp(withms=True):
    # todo: figure out if should use utc -> yes
    _t = time.time()
    ms = str(round(_t-int(_t),3))[1:]
    ms = '{:0<4}'.format(ms) # add 0's until have 3 digits + '.'
    base = time.strftime('%Y%m%d_%H%M%S',time.localtime(_t))
    return (base+ms) if(withms) else (base)

def load_config():
    ''' load config file and set settings. if doesn't exist, initialize '''
    path_conf = 'data/config.json' # hardcoding, not intended to be changed
    if(not osp.exists(path_conf)):
        # path doesn't exist, initialize file and settings
        if(not osp.dirname(path_conf)):
            os.mkdir(osp.dirname(path_conf))
        _d = {i:None for i in req_vals}
        with open(path_conf,'w') as f:
            json.dump(_d,f,indent=1)
        print("Config file doesn't exist, initialized.")
    with open(path_conf) as f:
        d = json.load(f)
    return d

def save_config(d:dict):
    for ireq in req_vals:
        assert ireq in d.keys(),"missing config value: "+ireq
    path_conf = 'data/config.json' # hardcoding, not intended to be changed
    with open(path_conf,'w') as f:
        json.dump(d,f,indent=1)

# eof
