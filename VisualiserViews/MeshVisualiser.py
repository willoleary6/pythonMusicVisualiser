import os

import numpy
import numpy as np
from pyqtgraph import Vector
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys
import wave

from opensimplex import OpenSimplex
import pyaudio
import struct

defaultframes = 512


class Terrain(object):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.window = gl.GLViewWidget()
        self.window.setGeometry(0, 110, 1920, 1080)
        self.window.show()
        self.window.setWindowTitle('terrain')
        self.window.setCameraPosition(distance=30, elevation=8)

        grid = gl.GLGridItem()
        grid.scale(2, 2, 2)
        self.window.addItem(grid)

        self.nstep = 1.9  # distance between each virtice
        self.ypoints = range(-20, 22, int(self.nstep))
        self.xpoints = range(-20, 22, int(self.nstep))

        self.nfaces = len(self.ypoints)  # what is used to loop over faces

        # audio
        self.sample_rate = 48000 #44.1 KH
        self.chunk = len(self.xpoints) * len(self.ypoints)

        self.p = pyaudio.PyAudio()

        # Open stream
        channelcount = 2
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=channelcount,
            rate= self.sample_rate,#int(device_info["defaultSampleRate"]),
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index= 7,# headphones 5,#device_info["index"],
            as_loopback=True
        )

        # perlin noise object
        self.noise = OpenSimplex()

        self.offset = 0

        verts, faces, colors = self.mesh()
        self.m1 = gl.GLMeshItem(
            vertexes=verts,
            faces=faces, faceColors=colors,
            smooth=False, drawEdges=True
        )

        self.m1.setGLOptions('additive')
        self.window.addItem(self.m1)

    def mesh(self, offset=0, height=1.5, wave_form_data = None):

        if wave_form_data is not None:

            wave_form_data = np.array(wave_form_data, dtype='int32') - 128 # centre at 0
            wave_form_data = wave_form_data * 0.00000008 # lower amplitude

            wave_form_data = wave_form_data.reshape((len(self.xpoints), len(self.ypoints)))
        else:
            wave_form_data = np.array([1] * 1764)
            wave_form_data = wave_form_data.reshape((len(self.xpoints), len(self.ypoints)))

        # populating vertices each point is gonna be a list
        verts = np.array([
            [
                x,
                y,
                wave_form_data[n][x] * self.noise.noise2d(x=n / 5 + offset, y=m / 5 + offset)  # this will be the noise value
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

        return verts, faces, colors

    def update(self):
        # populating vertices each point is gonna be a list
        wave_form_data = self.stream.read(self.chunk)


        #print(wave_form_data)

        audio_array = numpy.frombuffer(wave_form_data, dtype='int32')

        verts, faces, colors = self.mesh(
            offset=self.offset,
            wave_form_data= audio_array
        )
        self.m1.setMeshData(
            vertexes=verts,
            faces=faces, faceColors=colors,
            smooth=False, drawEdges=True
        )

        self.offset -= .00000001 # simulates movement

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
