# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import math
import sys
import numpy as np

import cv2
import ST7789 as ST7789

SPI_SPEED_MHZ = 80  # Higher speed = higher framerate

if len(sys.argv) > 1:
    SPI_SPEED_MHZ = int(sys.argv[1])

print("""
framerate.py - Test LCD framerate.

If you're using Breakout Garden, plug the 1.3" LCD (SPI)
breakout into the front slot.

Running at: {}MHz
""".format(SPI_SPEED_MHZ))

# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    rotation=90,
    spi_speed_hz=SPI_SPEED_MHZ * 1000000,
    using_opencv=True
)

WIDTH = disp.width
HEIGHT = disp.height
STEPS = WIDTH * 2
images = []

for step in range(STEPS):
    image = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
    image[:, :, 2] += 128

    if step % 2 == 0:
        image = cv2.rectangle(image, (120, 120), (240, 240), (0, 128, 0), 1) 
    else:
        image = cv2.rectangle(image, (0, 0), (119, 119), (0, 128, 0), 1) 

    f = math.sin((float(step) / STEPS) * math.pi)
    offset_left = int(f * WIDTH)
    image = cv2.ellipse(image, (offset_left + 5, 40), (5, 5), 0, 360, (255, 0, 0)) 

    images.append(image)

count = 0
time_start = time.time()

while True:
    disp.display(images[count % len(images)])
    count += 1
    time_current = time.time() - time_start
    if count % 120 == 0:
        print("Time: {:8.3f},      Frames: {:6d},      FPS: {:8.3f}".format(
            time_current,
            count,
            count / time_current))
