import os
import numpy as np
import picamera
from picamera.array import PiMotionAnalysis

QUEUE_SIZE = 10  # the number of consecutive frames to analyze
THRESHOLD = 100.0 # the minimum average magnitude of vectors across the frames

class MySpeedDetector(PiMotionAnalysis):
    def __init__(self, camera):
        super(MySpeedDetector, self).__init__(camera)
        self.x_queue = np.zeros(QUEUE_SIZE, dtype=np.float)
        self.y_queue = np.zeros(QUEUE_SIZE, dtype=np.float)

    def analyse(self, a):
        self.x_queue = np.roll(self.x_queue, 1)
        self.y_queue = np.roll(self.y_queue, 1)
        # If you want to detect objects that don't fill the camera's view,
        # limit the vectors that are considered here
        self.x_queue[0] = a['x'].mean()
        self.y_queue[0] = a['y'].mean()
        x_mean = self.x_queue.mean()
        y_mean = self.y_queue.mean()
        avg_speed = ((x_mean ** 2) + (y_mean ** 2) ** (1/2))
        if avg_speed > 100.0:
            print('Speeder detected: %.2f' % avg_speed)

with picamera.PiCamera() as camera:
    # Use the highest framerate possible, with a high enough resolution to
    # make out fast moving objects
    camera.resolution = (640, 480)
    camera.framerate = 90
    with MySpeedDetector(camera) as speed_detector:
        camera.start_recording(
            os.devnull, format='h264', motion_output=speed_detector)
        try:
            while True:
                camera.wait_recording(1)
        finally:
            camera.stop_recording()
