import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys


from opensimplex import OpenSimplex


class Terrain(object):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()
        self.w.setWindowTitle('terrain')
        self.w.setCameraPosition(distance=30, elevation=8)

        grid = gl.GLGridItem()
        grid.scale(2, 2, 2)
        self.w.addItem(grid)

        self.nstep = 1  # distance between each virtice
        self.ypoints = range(-20, 22, self.nstep)
        self.xpoints = range(-20, 22, self.nstep)

        self.nfaces = len(self.ypoints)  # what is used to loop over faces

        self.tmp = OpenSimplex()

        self.offset = 0

        # populating vertices each point is gonna be a list
        verts = np.array([
            [
                x,
                y,
                1.5 * self.tmp.noise2d(x=(n / 5) , y=(m / 5))  # this will be the noise value
            ] for n, x, in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
            # each loop iteration we create a list with 3 values for each x and y value
        ], dtype=np.float32)

        # populate the faces
        faces = []

        colors = []
        for m in range(self.nfaces - 1):
            # define y-offset
            yoff = m * self.nfaces
            for n in range(self.nfaces - 1):
                # adding faces to faces list
                faces.append([  # each face is a triangle, and eac of these is the corners of each triangle
                    n + yoff,
                    yoff + n + self.nfaces,
                    # adding nfaces as that will get us point 2 & 3 currently not on the current row
                    yoff + n + self.nfaces + 1
                ])

                faces.append([
                    n + yoff,
                    yoff + n + 1,
                    yoff + n + self.nfaces + 1
                ])

                colors.append([100, 100, 50, .2])
                colors.append([100, 100, 50, .2])

        faces = np.array(faces)
        colors = np.array(colors)
        self.m1 = gl.GLMeshItem(
            vertexes=verts,
            faces=faces, faceColors=colors,
            smooth=False, drawEdges=True
        )

        self.m1.setGLOptions('additive')
        self.w.addItem(self.m1)

    def update(self):

        # populating vertices each point is gonna be a list
        verts = np.array([
            [
                x,
                y,
                1.5 * self.tmp.noise2d(x=n / 5 + self.offset, y=m / 5 + self.offset)  # this will be the noise value
            ] for n, x, in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
            # each loop iteration we create a list with 3 values for each x and y value
        ], dtype=np.float32)

        # populate the faces
        faces = []

        colors = []
        for m in range(self.nfaces - 1):
            # define y-offset
            yoff = m * self.nfaces
            for n in range(self.nfaces - 1):
                # adding faces to faces list
                faces.append([  # each face is a triangle, and eac of these is the corners of each triangle
                    n + yoff,
                    yoff + n + self.nfaces,
                    # adding nfaces as that will get us point 2 & 3 currently not on the current row
                    yoff + n + self.nfaces + 1
                ])

                faces.append([
                    n + yoff,
                    yoff + n + 1,
                    yoff + n + self.nfaces + 1
                ])

                colors.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, .7])
                colors.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, .8])

        faces = np.array(faces)
        colors = np.array(colors)

        self.m1.setMeshData(
            vertexes=verts,
            faces=faces, faceColors=colors,
            smooth=False, drawEdges=True
        )

        self.offset -= 0.030 # simulates movement

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)
        self.start()
        self.update()

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    t = Terrain()
    t.animation()
