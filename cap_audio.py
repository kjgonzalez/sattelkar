'''
record audio for a specified amount of time
'''

import pyaudio
import wave
audio=pyaudio.PyAudio()

class AudioCapture:
    def __init__(self, filepath:str,format_=pyaudio.paInt16,rate=44100,frames_per_buffer=1024):
        '''
        Given save location & audio properties, start recording audio
          filepath: where to save file. must end with .wav

        '''
        # imitating vid: activate audio device, initialize destination file
        self.path = filepath
        self._audio = pyaudio.PyAudio()
        nchannel = 2
        self.cap = self._audio.open(format=format_, channels=nchannel, rate=rate, input=True,
                               frames_per_buffer=frames_per_buffer) # initialize audio device
        assert '.wav' in self.path,"invalid file format"
        self.out = wave.open(self.path,'wb')
        self.out.setnchannels(nchannel)
        self.out.setsampwidth(audio.get_sample_size(format_))
        self.out.setframerate(rate) # initialize audio file
        self.frames_per_buffer = frames_per_buffer
        self.chunks_per_sec = rate/frames_per_buffer

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

if(__name__ == '__main__'):
    # print('hello')
    a = AudioCapture('data/aud.wav')
    print('starting audio')
    a.record_n_seconds(5)
    print('stopped audio, data saved')
