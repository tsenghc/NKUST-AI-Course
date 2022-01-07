import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
from tqdm import tqdm
from numpy.random import rand


class K_means:
    def __init__(self, n_clusters, max_iter=1, random_seed=111) -> None:
        np.random.seed(random_seed)
        self.iter_count = 0
        self.point_for_cluster = {}
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_seed = random_seed
        self.center_point = \
            np.random.randint(
                0, 255, size=(self.n_clusters, 3))

    def read_img(self, file_path) -> np.array:
        img = cv2.imread(filename=file_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.array(img)
        self.data = img.reshape(
            img.shape[0]*img.shape[1], img.shape[2])
        return img, img.shape

    def euclidean_distance(self, pointA, pointB, _norm=np.linalg.norm):
        return _norm(pointA - pointB)

    def draw_scatter(img):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        for i in img:
            ax.scatter(i[0], i[1], i[2])
        plt.show()

    def draw_img(self, img):
        plt.imshow(img)
        plt.show()

    def move_center(self):
        self.new_center_point = {}
        for k, data_point in enumerate((self.data)):
            _temp = []
            for center_point in self.center_point:
                _temp.append(KM.euclidean_distance(center_point, data_point))
            self.point_for_cluster[k] = _temp.index(min(_temp))

        for i in range(self.n_clusters):
            _temp = []
            for k, v in (self.point_for_cluster.items()):
                if i == v:
                    _temp.append(self.data[k])
            if len(_temp) > 0:
                self.center_point[i] = np.array(_temp).mean(axis=0)
        print(self.center_point)

    def calu(self):
        new_img = []
        for i in tqdm(range(self.max_iter)):
            KM.move_center()
        for k in range(len(self.data)):
            new_img.append(self.center_point[self.point_for_cluster[k]])
        return new_img


if __name__ == '__main__':
    KM = K_means(n_clusters=3, max_iter=1, random_seed=np.random.randint(10000))
    raw_img, raw_img_shape = KM.read_img("image002.jpg")
    raw_img = np.reshape(raw_img, (raw_img_shape[0], raw_img_shape[1], 3))

    print(raw_img.shape)
    out_img = KM.calu()
    out_img = np.reshape(out_img, (raw_img_shape[0], raw_img_shape[1], 3))
    # plt.imsave('out_img002_cluster_3.jpg', out_img.astype(np.uint8))
    fig = plt.figure(figsize=(8, 4))
    fig.add_subplot(1, 2, 1)
    plt.imshow(raw_img)
    fig.add_subplot(1, 2, 2)
    plt.imshow(out_img)
    # plt.savefig('outme.jpg', dpi=100)
    plt.show()
    # sys.exit()
