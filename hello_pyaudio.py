'''

sample of first time recording audio in python


import pyaudio
import pyaudio
audio = pyaudio.PyAudio()

def recaudio(nsec=10):
    stream=audio.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=1024)
    print('starting...')
    frames=[]
    for i in range(0,int(44100/1024*nsec)):
        data=stream.read(1024)
        frames.append(data)
    print('done')
    stream.stop_stream()
    stream.close()
    audio.terminate()
import wave
def recaudio(nsec=10):
    stream=audio.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=1024)
    print('starting...')
    frames=[]
    for i in range(0,int(44100/1024*nsec)):
        data=stream.read(1024)
        frames.append(data)
    print('done')
    stream.stop_stream()
    stream.close()
    audio.terminate()
    fw = wave.open('test.wav','wb')
    fw.setnchannels(2)
    fw.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    fw.setframerate(44100)
    fw.writeframes(b''.join(frames))
    fw.close()
    print('file created')
recaudio()

'''
import pyaudio
import wave
audio = pyaudio.PyAudio()

def recaudio(nsec=10):
    stream=audio.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=1024)
    print('starting...')
    frames=[]
    for i in range(0,int(44100/1024*nsec)):
        data=stream.read(1024)
        frames.append(data)
    print('done')
    stream.stop_stream()
    stream.close()
    audio.terminate()
def recaudio(nsec=10):
    stream=audio.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=1024)
    print('starting...')
    frames=[]
    for i in range(0,int(44100/1024*nsec)):
        data=stream.read(1024)
        frames.append(data)
    print('done')
    stream.stop_stream()
    stream.close()
    audio.terminate()
    fw = wave.open('data/test.wav','wb')
    fw.setnchannels(2)
    fw.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    fw.setframerate(44100)
    fw.writeframes(b''.join(frames))
    fw.close()
    print('file created')
recaudio()


print('check text')