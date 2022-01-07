import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import datasets
# create datasets
import cv2


class DBSCAN:
    def __init__(self, eps, minpts) -> None:
        self.eps = eps
        self.minpts = minpts
        self.dataset = None

    def read_img(self, file_path) -> np.array:
        img = cv2.imread(filename=file_path)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = np.array(img)
        self.data = img.reshape(-1, 3)
        return img, img.shape

    def data_gen(self):
        X, y = datasets.make_blobs(n_samples=50, centers=3,
                                   n_features=2, random_state=20, cluster_std=1.5)
        self.dataset = X
        return X

    def draw_img(self, img):
        plt.scatter(img[:, 0], img[:, 1],  cmap='plasma')
        plt.show()


if __name__ == "__main__":
    dbscan = DBSCAN(eps=2, minpts=5)
    img = dbscan.read_img("Demo1.bmp")
    # img = dbscan.data_gen()
    dbscan.draw_img(img)
