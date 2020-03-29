import sys
import time
import threading

from PyQt5.QtWidgets import QApplication

from DebugVisualiser.DebugVisualiser import DebugVisualiser
from random import randrange

app = QApplication(sys.argv)
visualiser = DebugVisualiser()



for x in range(0,10):
    r = randrange(254)
    g = randrange(254)
    b = randrange(254)
    time.sleep(1)
    visualiser.updateBackgroundColor(r,g,b)
sys.exit(app.exec_())