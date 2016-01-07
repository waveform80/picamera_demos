==============
Picamera Demos
==============

This repository contains a selection of scripts for use with the `picamera`_
library. These scripts were considered a bit long for inclusion in the
documentation (at the time of writing), and were previously stuck in various
gists which weren't easy to locate online.

The contents of the repository currently includes:

color_detect.py
    A simple script which tries to work out what color it can see in the center
    of the camera's preview.

gesture_detect.py
    A script which detects rudimentary hand motions in front of the camera;
    left, right, up, and down or combinations of the above.

motion_detect.py
    The simplest motion detector which triggers when enough motion estimation
    vectors exceed a set threshold.

speed_detect.py
    A demonstration of calculating "speed" (in pixels/frame) of objects in the
    field of view.

.. _picamera: https://picamera.readthedocs.org/

License
=======

The contents of the picamera demos repository are public domain; I waive any
interest or copyright over the contents.

