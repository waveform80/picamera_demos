import os
import numpy as np
import picamera
from picamera.array import PiMotionAnalysis

QUEUE_SIZE = 10  # the number of consecutive frames to analyze
THRESHOLD = 4.0  # the minimum average motion required in either axis

class MyGestureDetector(PiMotionAnalysis):
    def __init__(self, camera):
        super(MyGestureDetector, self).__init__(camera)
        self.x_queue = np.zeros(QUEUE_SIZE, dtype=np.float)
        self.y_queue = np.zeros(QUEUE_SIZE, dtype=np.float)

    def analyse(self, a):
        # Roll the queues and overwrite the first element with a new
        # mean (equivalent to pop and append)
        self.x_queue = np.roll(self.x_queue, 1)
        self.y_queue = np.roll(self.y_queue, 1)
        self.x_queue[0] = a['x'].mean()
        self.y_queue[0] = a['y'].mean()
        # Calculate the mean of both queues
        x_mean = self.x_queue.mean()
        y_mean = self.y_queue.mean()
        # Convert left/up to -1, right/down to 1, and movement below
        # the threshold to 0
        x_move = ('' if abs(x_mean) < THRESHOLD else 'left' if x_mean < 0.0 else 'right')
        y_move = ('' if abs(y_mean) < THRESHOLD else 'up'   if y_mean < 0.0 else 'down')
        # Update the display
        self.camera.annotate_text = '%s %s' % (x_move, y_move)

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 24
    with MyGestureDetector(camera) as gesture_detector:
        camera.start_recording(
            os.devnull, format='h264', motion_output=gesture_detector)
        try:
            while True:
                camera.wait_recording(1)
        finally:
            camera.stop_recording()
