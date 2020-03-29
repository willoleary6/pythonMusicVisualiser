from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication
from PyQt5.QtWidgets import QMainWindow
from win32api import GetSystemMetrics


class _UpdateUiBackgroundColor(QObject):
    updateSignal = pyqtSignal(int, int, int)


class DebugVisualiser(QMainWindow):

    def __init__(self):
        super().__init__()
        self.connection = _UpdateUiBackgroundColor()
        self.connection.updateSignal.connect(self._update_ui_color)
        self.setGeometry(
            int(GetSystemMetrics(0) * .4),  # left
            int(GetSystemMetrics(1) * .4),  # top
            int(GetSystemMetrics(0) * .2),  # height
            int(GetSystemMetrics(1) * .2)  # width
        )
        self.setWindowTitle('Color')
        self.show()

    def _update_ui_color(self, red, green, blue):
        p = QPalette()
        p.setColor(self.backgroundRole(), QColor(red, green, blue))
        self.setPalette(p)
        # force the UI to update
        QCoreApplication.processEvents()

    def update_color(self, r, g, b):
        self.connection.updateSignal.emit(r, g, b)
