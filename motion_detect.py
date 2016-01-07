import os
import picamera
import numpy as np
from picamera.array import PiMotionAnalysis

# A simple demo of sub-classing PiMotionAnalysis to construct a motion detector

MOTION_MAGNITUDE = 60   # the magnitude of vectors required for motion
MOTION_VECTORS = 10     # the number of vectors required to detect motion

class MyMotionDetector(PiMotionAnalysis):
    def analyse(self, a):
        # Calculate the magnitude of all vectors with pythagoras' theorem
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # Count the number of vectors with a magnitude greater than our
        # threshold
        vector_count = (a > MOTION_MAGNITUDE).sum()
        if vector_count > MOTION_VECTORS:
            print('Detected motion!')

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    with MyMotionDetector(camera) as motion_detector:
        camera.start_recording(
            os.devnull, format='h264', motion_output=motion_detector)
        try:
            while True:
                camera.wait_recording(1)
        finally:
            camera.stop_recording()
