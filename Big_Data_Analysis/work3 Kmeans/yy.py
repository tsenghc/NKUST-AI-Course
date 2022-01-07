from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import OpenGL.GL as ogl
import numpy as np

class CustomTextItem(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, X, Y, Z, text):
        gl.GLGraphicsItem.GLGraphicsItem.__init__(self)
        self.text = text
        self.X = X
        self.Y = Y
        self.Z = Z

    def setGLViewWidget(self, GLViewWidget):
        self.GLViewWidget = GLViewWidget

    def setText(self, text):
        self.text = text
        self.update()

    def setX(self, X):
        self.X = X
        self.update()

    def setY(self, Y):
        self.Y = Y
        self.update()

    def setZ(self, Z):
        self.Z = Z
        self.update()

    def paint(self):
        self.GLViewWidget.qglColor(QtCore.Qt.black)
        self.GLViewWidget.renderText(self.X, self.Y, self.Z, self.text)


class Custom3DAxis(gl.GLAxisItem):
    """Class defined to extend 'gl.GLAxisItem'."""
    def __init__(self, parent, color=(0,0,0,.6)):
        gl.GLAxisItem.__init__(self)
        self.parent = parent
        self.c = color

    def draw_labels(self):
        x,y,z = self.size()
        #X label
        self.xLabel = CustomTextItem(X=x/2, Y=-y/20, Z=-z/20, text="X")
        self.xLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.xLabel)
        #Y label
        self.yLabel = CustomTextItem(X=-x/20, Y=y/2, Z=-z/20, text="Y")
        self.yLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.yLabel)
        #Z label
        self.zLabel = CustomTextItem(X=-x/20, Y=-y/20, Z=z/2, text="Z")
        self.zLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.zLabel)

    def paint(self):
        self.setupGLState()
        if self.antialias:
            ogl.glEnable(ogl.GL_LINE_SMOOTH)
            ogl.glHint(ogl.GL_LINE_SMOOTH_HINT, ogl.GL_NICEST)
        ogl.glBegin(ogl.GL_LINES)

        x,y,z = self.size()
        #Draw Z
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, 0, z)
        #Draw Y
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, y, 0)
        #Draw X
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(x, 0, 0)
        #Draw labels
        self.draw_labels()
        ogl.glEnd()


app = QtGui.QApplication([])
fig1 = gl.GLViewWidget()
background_color = app.palette().color(QtGui.QPalette.Background)
fig1.setBackgroundColor(background_color)

n = 51
y = np.linspace(-10,10,n)
x = np.linspace(-10,10,100)
for i in range(n):
    yi = np.array([y[i]]*100)
    d = (x**2 + yi**2)**0.5
    z = 10 * np.cos(d) / (d+1)
    pts = np.vstack([x,yi,z]).transpose()
    plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((i,n*1.3)), width=(i+1)/10., antialias=True)
    fig1.addItem(plt)


axis = Custom3DAxis(fig1, color=(0.2,0.2,0.2,.6))
axis.setSize(x=12, y=12, z=12)
fig1.addItem(axis)
fig1.opts['distance'] = 40

fig1.show()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()