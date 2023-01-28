'''
Sattelkar Monitor
A long-term audio/video monitoring program
Kristian Gonzalez, 2022
-------------------

Main running script for output

general steps: 
1. turn on
2. activate audio and video capabilities
3. locate save location
4. begin recording

stat-description
done find export folder
done record data
done combine data
done label correctly
done set frequency
todo remove all debug settings
todo add screen aliases for ease of use
todo enable wifi connection
todo consider running video/audio until both finish, not cutting off longer one
done create path to export if doesn't already exist
'''

import os
import argparse
import time
from cap_av import record_n_seconds
from cap_video import tstamp
osp  = os.path
path_export='/media/pi/hdd5tb/data_sattelkar'

def print_wTime(msg):
    ''' simple way of printing text with embedded timestamp'''
    print(f'{tstamp(False)}: {msg}')

if(__name__=='__main__'):
    # initialize program
    p=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--stopafter',default='0s',help='number of seconds or days to stop after, e.g. 3600s or 5d')
    args=p.parse_args()
    print('SATTELKAR MONITOR PROGRAM\n')
    print('Arguments:')
    for iarg in [i for i in dir(args) if(i[0] != '_')]: 
        print(f'  {iarg}: {getattr(args,iarg)}')
    PER=int(args.per)
    PATHOUT=args.path_export
    NDAYS=int(args.stopafter)

    # initial setup of components ==============================================
    t_program_start=time.time()
    # todo: load config from config.json file

    # main loop ================================================================
    done=False
    while(not done):
        print_wTime('starting recording... ')
        record_n_seconds(path_folder=PATHOUT,duration_s=PER)

        if(NDAYS!=-1 and (time.time()-t_program_start)/86400>NDAYS):
            done=True

        elif(time.time()-t_program_start > 3600): # todo: remove debugging
            done = True
    print_wTime('time limit reached, program exiting')

# eof
