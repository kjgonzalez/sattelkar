'''
record audio for a specified amount of time
'''

from ctypes import * # error / warning suppression
import pyaudio
import wave
audio=pyaudio.PyAudio()

# src: https://stackoverflow.com/questions/33985863/hiding-console-output-produced-by-os-system
# # From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
# # $ grep -rn snd_lib_error_handler_t
# # include/error.h:59:typedef void (*snd_lib_error_handler_t)(const char *file, int line, const char *function, int err, const char *fmt, ...) /* __attribute__ ((format (printf, 5, 6))) */;
# # Define our error handler type
# ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
# def py_error_handler(filename, line, function, err, fmt):
#     print('messages are yummy')
# c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
#
# asound = cdll.LoadLibrary('libasound.so')
# # Set error handler
# asound.snd_lib_error_set_handler(c_error_handler)

class CaptureAudio:
    def __init__(self, src=0, format_=pyaudio.paInt16, rate=44100, bufsize=1024,nchannel=1,
                 verbose=False):
        '''
        Given save location & audio properties, start recording audio
          filepath: where to save file. must end with .wav

        note on default values: tuning for compatability with sattelkar hardware
        '''
        self._src = src
        self._audio = pyaudio.PyAudio()
        self._format=format_
        self._rate = rate
        self._bufsize = bufsize
        self._nchannel = nchannel
        self._cap:pyaudio.Stream=None
        self._v = verbose
    def opencap(self):
        self._cap = self._audio.open(format=self._format, channels=self._nchannel,
                                     rate=self._rate, input=True,
                                     frames_per_buffer=self._bufsize, input_device_index=self._src)
        return True # capture is ready

    def closecap(self):
        self._audio.terminate()
        self._cap.stop_stream()
        self._cap.close()

    def record_n_seconds(self,filepath:str, nseconds:int):
        ''' asking to record n seconds is really asking to record a number of chunks '''
        assert '.wav' in filepath, "invalid file format"

        nchunks = int(self._rate / self._bufsize * nseconds)
        frames=[]

        for ichunk in range(nchunks):
            data = self._cap.read(self._bufsize,exception_on_overflow=False) # todo: to lose data?
            frames.append(data)
            # out.writeframes(data)

        # save all data
        out = wave.open(filepath, 'wb')
        out.setnchannels(self._nchannel)
        out.setsampwidth(audio.get_sample_size(self._format))
        out.setframerate(self._rate)  # initialize audio file
        for iframe in frames:
            out.writeframes(iframe)
        out.close()
        if(self._v): print(f'out: {filepath}')

def choose_audio_source():
    print('list of audio sources, select the number of desired audio source: ')
    _p = pyaudio.PyAudio()
    info = _p.get_host_api_info_by_index(0)
    devicetuples = []
    for i in range(info.get('deviceCount')):
        idev = _p.get_device_info_by_host_api_device_index(0, i)
        if (idev.get('maxInputChannels')) > 0:
            iname = idev.get('name')
            devicetuples.append((i, iname))
            print('{}: {} (nchannels: {})'.format(*devicetuples[-1],idev.get('maxInputChannels')))
    res = input('audio source: ')
    if(res == 'd'): return res
    elif(res == ''): return res
    return int(res)

def check_audio(path):
    # todo: check properties of audio file created
    pass

if(__name__ == '__main__'):
    import argparse
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--srcpick',default=False,action='store_true',
                   help='initialize with choice of sources')
    args = p.parse_args()
    source_val = 0
    if(args.srcpick):
        source_val = choose_audio_source()
        print('you chose:',source_val)

    a = CaptureAudio(src=source_val)
    print('ready?',a.opencap())
    a.record_n_seconds('data/out.wav',3)
    print('first done')
    a.record_n_seconds('data/out2.wav',3)
    print('stopped audio, data saved')
