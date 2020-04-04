import time

import soundcard
import numpy
import sys

from PyQt5.QtWidgets import QApplication

from DebugVisualiser.DebugVisualiser import DebugVisualiser

numpy.set_printoptions(threshold=sys.maxsize)
input = soundcard.all_microphones(include_loopback=True)[0]
samplerate = 48000
chunk = 1024

#print(object_methods)
print(input)
print(input.recorder(samplerate))
default_speaker = soundcard.default_speaker()

data = input.record(samplerate=48000, numframes=48000)
default_speaker.play(data/numpy.max(data), samplerate=48000)
app = QApplication(sys.argv)
visualiser = DebugVisualiser()
# alternatively, get a `Recorder` and `Player` object
# and play or record continuously:
with input.recorder(samplerate=48000) as mic, \
      default_speaker.player(samplerate=48000) as sp:
    while True:
        data = mic.record(numframes=1024)
        data = [data[:, 0].mean(), data[:, 0].mean()]
        print(data)

        visualiser.update_color(abs(data[0]*10000), abs(data[0]*10000), abs(data[0]*10000))



sys.exit(app.exec_())