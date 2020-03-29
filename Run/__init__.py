import sys
import time
import threading

from PyQt5.QtWidgets import QApplication

from DebugVisualiser.DebugVisualiser import DebugVisualiser
from random import randrange

app = QApplication(sys.argv)
visualiser = DebugVisualiser()

while True:
    for r in range(255):
        visualiser.update_color(r, 0, 0)
        time.sleep(0.01)
    for g in range(255):
        visualiser.update_color(0, g, 0)
        time.sleep(0.01)
    for b in range(255):
        visualiser.update_color(0, 0, b)
        time.sleep(0.01)


sys.exit(app.exec_())
