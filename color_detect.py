import picamera
import numpy as np
from operator import itemgetter
from picamera.array import PiRGBAnalysis
from picamera.color import Color

THRESHOLD = 5.0
COLORS = {
    Color('#800'): 'red',
    Color('#080'): 'green',
    Color('#008'): 'blue',
    }

class MyColorAnalyzer(PiRGBAnalysis):
    def __init__(self, camera):
        super(MyColorAnalyzer, self).__init__(camera)
        self.last_color = 'none'

    def analyse(self, a):
        # Calculate the average color of the pixels in the middle box
        sample = Color(
            r=int(np.mean(a[30:60, 60:120, 0])),
            g=int(np.mean(a[30:60, 60:120, 1])),
            b=int(np.mean(a[30:60, 60:120, 2]))
            )
        # Calculate matches, find the closest and check if it's below a
        # threshold difference
        matches = {
            sample.difference(color, method='cie1976'): name
            for color, name in COLORS.items()
            }
        matches = sorted(matches.items(), key=itemgetter(1))
        if matches[0][0] < 5.0:
            color = matches[0][1]
        else:
            color = 'none'
        # If the color has changed, update the display
        if color != self.last_color:
            self.camera.annotate_text = color
            self.last_color = color

with picamera.PiCamera() as camera:
    camera.resolution = (160, 90)
    camera.framerate = 24
    # Fix the camera's white-balance gains
    camera.awb_mode = 'off'
    camera.awb_gains = (1.4, 1.5)
    # Draw a box over the area we're going to watch
    camera.start_preview(alpha=128)
    box = np.zeros((96, 160, 3), dtype=np.uint8)
    box[30:31, 60:120, :] = 0xff
    box[60:61, 60:120, :] = 0xff
    box[30:60, 60:61, :] = 0xff
    box[30:60, 120:121, :] = 0xff
    camera.add_overlay(memoryview(box), size=(160, 90), layer=3, alpha=64)
    # Construct the analysis output and start recording data to it
    with MyColorAnalyzer(camera) as color_analyzer:
        camera.start_recording(color_analyzer, 'rgb')
        while True:
            camera.wait_recording(1)
        camera.stop_recording()
