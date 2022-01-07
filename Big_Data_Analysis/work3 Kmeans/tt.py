from numpy.random import randn, random
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import cv2


img = cv2.imread("5k.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = np.array(img)
img.astype('int')
print(img.shape)
img = img.reshape(img.shape[0]*img.shape[1], img.shape[2])
print(img.shape)

app = QtGui.QApplication([])
view = gl.GLViewWidget()
view.show()
x_grid = gl.GLGridItem()
y_grid = gl.GLGridItem()
z_grid = gl.GLGridItem()
y_grid.rotate(90, 0, 1, 0)
z_grid.rotate(90, 1, 0, 0)
view.addItem(x_grid)
view.addItem(y_grid)
view.addItem(z_grid)

# generate random points from -10 to 10, z-axis positive
pos = np.random.random(size=(100, 3))
print(pos.shape)
# img *= [10,10,10]
# img[0] = (0, 0, 0)
color = np.ones((img.shape[0], 4))

size = np.random.random(size=img.shape[0])*10
sp2 = gl.GLScatterPlotItem(pos=img, color=(0.5, 0.75, 0.5, 0.35), size=size)
view.addItem(sp2)

def update():
    sp2.setData(pos=img)


t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
