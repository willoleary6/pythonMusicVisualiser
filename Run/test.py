import sys
import threading
import time
from random import randrange

from PyQt5.QtWidgets import QApplication

from DebugVisualiser.DebugVisualiser import DebugVisualiser


class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.app = QApplication(sys.argv)
        self.visualiser = DebugVisualiser()
        self.r = 0
        self.g = 0
        self.b = 0
        self.proceed = True
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            self.visualiser.updateBackgroundColor(self.r, self.g, self.b)

            #time.sleep(self.interval)

example = ThreadingExample()

print("adjusting now \n")

for i in range(255):
    example.r = i



sys.exit(example.app.exec_())

#https://stackoverflow.com/questions/52073973/how-do-i-update-the-gui-from-another-thread-using-python