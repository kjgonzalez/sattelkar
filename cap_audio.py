'''
record audio for a specified amount of time
'''

import pyaudio
import wave
audio=pyaudio.PyAudio()

class AudioCapture:
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
        out = wave.open(filepath, 'wb')
        out.setnchannels(self._nchannel)
        out.setsampwidth(audio.get_sample_size(self._format))
        out.setframerate(self._rate)  # initialize audio file

        nchunks = int(self._rate / self._bufsize * nseconds)
        for ichunk in range(nchunks):
            data = self._cap.read(self._bufsize,exception_on_overflow=False) # todo: to lose data?
            out.writeframes(data)

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
    return int(input('audio source: '))

def check_audio(path):
    # todo: check properties of audio file created
    pass

if(__name__ == '__main__'):
    import argparse
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--srcpick',default=False,action='store_true',
                   help='initialize with choice of sources')
    args = p.parse_args()
    val = 0
    if(args.srcpick):
        val = choose_audio_source()
        print('you chose:',val)

    a = AudioCapture(src=val)
    print('ready?',a.opencap())
    a.record_n_seconds('data/out.wav',3)
    print('first done')
    a.record_n_seconds('data/out2.wav',3)
    print('stopped audio, data saved')
