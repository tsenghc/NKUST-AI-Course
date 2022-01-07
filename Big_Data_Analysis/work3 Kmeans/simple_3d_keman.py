import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import size
import pyqtgraph.opengl as gl
from numpy.random import rand
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from random import sample
app = QtGui.QApplication([])
view = gl.GLViewWidget()
# pg.setConfigOptions(antialias=True)
view.show()


class K_means:
    def __init__(self, n_clusters, max_iter=100, random_seed=111, center_min=0, center_max=10) -> None:
        np.random.seed(random_seed)
        self.iter_count = 0
        self.center_point_color = []
        self.point_for_cluster = {}
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_seed = random_seed
        self.center_point = \
            np.random.uniform(
                low=center_min, high=center_max, size=(self.n_clusters, 3))

    def use_pyqt_draw(self, data, point_size):
        x_grid = gl.GLGridItem()
        y_grid = gl.GLGridItem()
        z_grid = gl.GLGridItem()
        y_grid.rotate(90, 0, 1, 0)
        z_grid.rotate(90, 1, 0, 0)
        # view.addItem(x_grid)
        # view.addItem(y_grid)
        # view.addItem(z_grid)
        size = np.random.random(data.shape[0])*20
        plot_item = gl.GLScatterPlotItem(
            pos=data, color=(1, 1, 1, 0.5), size=size)
        view.addItem(plot_item)
        view.addItem(gl.GLAxisItem(size=QtGui.QVector3D(
            255, 255, 255), glOptions="opaque"))
        self.pyqt_plot_item = plot_item
        self.data = data
        self.point_size = point_size
        self.raw_data_color = np.reshape(
            [1, 1, 1, 0.5]*len(self.data), (len(self.data), 4))
        center_point_RGB = np.random.uniform(
            low=0.3, high=1, size=(self.n_clusters, 3))
        for k, v in enumerate(center_point_RGB):
            center_point_color = np.append(np.array(v), np.array([1]))
            self.center_point_color.append(center_point_color)

    def update(self):
        data = np.concatenate([self.data, self.center_point])
        color = np.concatenate([self.raw_data_color, self.center_point_color])
        self.pyqt_plot_item.setData(
            pos=data, color=color, size=(self.point_size))

        if self.max_iter >= self.iter_count:
            self.iter_count += 1
            print(self.iter_count)
            KM.move_center()
        pass

    def gen_sample(self, sample, min, max) -> np.array:
        return np.random.uniform(low=min, high=max, size=(self.n_clusters, sample, 3))

    def euclidean_distance(self, pointA, pointB, _norm=np.linalg.norm):
        return _norm(pointA - pointB)

    def draw_scatter(self, data):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        for i in data:
            ax.scatter(i[0], i[1], i[2])
        plt.show()

    def draw_data(self, data):
        plt.imshow(data)
        plt.show()

    def move_center(self):
        center_point_distance = {}

        for k, data_point in enumerate((self.data)):
            _temp = []
            for center_point in self.center_point:
                _temp.append(KM.euclidean_distance(center_point, data_point))
            self.point_for_cluster[k] = _temp.index(min(_temp))

        for k, v in self.point_for_cluster.items():
            self.raw_data_color[k][0:3] = self.center_point_color[v][0:3]

        for i in range(self.n_clusters):
            _temp = []
            for k, v in self.point_for_cluster.items():
                if i == v:
                    _temp.append(self.data[k])
            if len(_temp)>0:
                self.center_point[i] = np.array(_temp).mean(axis=0)
        print(self.center_point)

    def read_img(self, file_path) -> np.array:
        img = cv2.imread(filename=file_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.array(img)
        print(img.shape)
        return img


if __name__ == '__main__':
    KM = K_means(n_clusters=32, max_iter=5, random_seed=111,
                 center_min=1, center_max=255)
    raw_img = KM.read_img("test_img1.jpg")
    raw_img = raw_img.reshape(
        raw_img.shape[0]*raw_img.shape[1], raw_img.shape[2])
    raw_img = raw_img[np.random.choice(raw_img.shape[0], size=10000), :]

    raw_data = KM.gen_sample(sample=100, min=0, max=50)
    raw_data = raw_data.reshape(
        raw_data.shape[0]*raw_data.shape[1], raw_data.shape[2])
    print(raw_data.shape, raw_img.shape)
    KM.use_pyqt_draw(raw_img, point_size=5)
    t = QtCore.QTimer()
    t.timeout.connect(KM.update)
    t.start(5000)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
