'''
record audio for a specified amount of time
'''

import pyaudio
import wave
audio=pyaudio.PyAudio()

class AudioCapture:
    def __init__(self, filepath:str, src=0, format_=pyaudio.paInt16, rate=44100, bufsize=1024):
        '''
        Given save location & audio properties, start recording audio
          filepath: where to save file. must end with .wav
        '''
        # todo: need way to select audio device / source
        # imitating vid: activate audio device, initialize destination file
        self.path = filepath
        self._audio = pyaudio.PyAudio()
        nchannel = 2
        # initialize audio device
        self.cap = self._audio.open(format=format_, channels=nchannel, rate=rate, input=True,
                                    frames_per_buffer=bufsize, input_device_index=src)
        assert '.wav' in self.path,"invalid file format"
        self.out = wave.open(self.path,'wb')
        self.out.setnchannels(nchannel)
        self.out.setsampwidth(audio.get_sample_size(format_))
        self.out.setframerate(rate) # initialize audio file
        self.frames_per_buffer = bufsize
        self.chunks_per_sec = rate / bufsize

    def opencap(self):
        # todo: consider if having specific file to initialie capture is worth it
        pass
    def record_n_seconds(self,nseconds:int):
        ''' asking to record n seconds is really asking to record a number of chunks '''
        nchunks = int(self.chunks_per_sec * nseconds)
        for ichunk in range(nchunks):
            data = self.cap.read(self.frames_per_buffer)
            self.out.writeframes(data)
        self.cap.stop_stream()
        self.cap.close()
        self._audio.terminate()
        self.out.close()

def choose_audio_source():
    print('list of sources, select the number of desired audio source: ')
    _p = pyaudio.PyAudio()
    info = _p.get_host_api_info_by_index(0)
    devicetuples = []
    for i in range(info.get('deviceCount')):
        idev = _p.get_device_info_by_host_api_device_index(0, i)
        if (idev.get('maxInputChannels')) > 0:
            iname = idev.get('name')
            devicetuples.append((i, iname))
            print('{}: {}'.format(*devicetuples[-1]))
    return int(input('source: '))


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

    a = AudioCapture('data/aud.wav',src=val)
    print('starting audio')
    a.record_n_seconds(5)
    print('stopped audio, data saved')
