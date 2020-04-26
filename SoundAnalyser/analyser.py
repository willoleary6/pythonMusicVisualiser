
import sys

from PyQt5.QtWidgets import QApplication

from VisualiserViews.MeshVisualiser import Terrain

app = QApplication(sys.argv)
visualiser = Terrain()


sys.exit(app.exec_())