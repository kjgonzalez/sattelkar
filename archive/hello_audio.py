'''
sample of first time recording audio in python
'''
import pyaudio
import wave
audio = pyaudio.PyAudio()

_tmax = 5 # seconds

def recaudio(nsec=10):
    stream=audio.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=1024)


    frames=[]
    for i in range(0,int(44100/1024*nsec)):
        data=stream.read(1024)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    fw = wave.open('data/hello_audio.wav','wb')
    fw.setnchannels(2)
    fw.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    fw.setframerate(44100)
    fw.writeframes(b''.join(frames))
    fw.close()

print('starting...')
recaudio(30)
print('done')
