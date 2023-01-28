import picamera
import numpy as np
stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.resolution = (320,240)
    camera.capture(stream,format='jpeg')
buff = np.frombuffer(stream.getvalue(),dtype=numpy.uint8)
print('done'
