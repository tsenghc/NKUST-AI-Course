import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import copy
from sklearn import datasets
import tqdm
import copy
import time


class DBSCAN:
    def __init__(self, eps, minpts) -> None:
        self.eps = eps
        self.minpts = minpts
        self.dataset = None
        self.stack = []
        self.scaned = []

    def read_img(self, file_path) -> np.array:
        img = cv2.imread(filename=file_path)
        self.img_shape = img.shape

        return img

    def data_gen(self):
        X, y = datasets.make_blobs(n_samples=50, centers=3,
                                   n_features=2, random_state=20, cluster_std=1.5)
        self.dataset = X
        return X

    def draw_scatter(self, img):
        plt.scatter(img[:, 0], img[:, 1], cmap='plasma')
        plt.show()

    def draw_img(self, img):
        plt.imshow(img)
        plt.show()

    def dbscan_preprocess(self, img):
        img = img.reshape(-1, 3)[:, 0]
        # background = np.where(img == 255)
        point = np.where(img == 0)
        y_len = np.full(point[0].shape[0], self.img_shape[1], dtype=int)
        point_row_index = point//y_len
        point_col_index = point % y_len
        self.index_list = np.array(
            list(zip(point_col_index[0], point_row_index[0])), dtype=np.uint16)

    def min_distance(self, point):
        distance_1d = np.power(np.subtract(
            point, self.index_list, dtype=np.float32), 2).sum(axis=1)
        distance_1d = np.power(distance_1d, 0.5)
        min_distance = np.where(distance_1d <= self.eps)[0]
        return min_distance

    def dbscan(self):
        _temp = []
        core_point = []
        color_id = {}
        point_id = []
        already_scan = []
        color_num = 0
        for i in tqdm.tqdm(self.index_list):
            min_distance = DBSCAN.min_distance(i)
            _temp.append(min_distance)

        for pair_point in _temp:
            if pair_point.shape[0] >= self.minpts:
                core_point.append(pair_point)

        print("core_point", len(core_point))

        while len(already_scan) != len(core_point):
            _stack = []
            point_index = []
            for pk, p in enumerate(core_point):
                for _ in p:
                    _stack.append(_)

                for _ in _stack:
                    point_id.append(core_point[_])

                # if pk in already_scan:
                #     continue
                # if any(point_index):
                #     if not any(np.intersect1d(np.array(p), np.array(point_index))):
                #         continue

                # for _ in p:
                #     if _ in point_index:
                #         continue
                #     point_index.append(_)
                # if pk in already_scan:
                #     continue
                # already_scan.append(pk)

            color_id[color_num] = point_index
            color_num += 1
            print(len(already_scan), color_num)

        for k, v in color_id.items():
            color_id[k] = [self.index_list[i].tolist() for i in v]

        plt.figure()
        x = []
        y = []
        color_lable = []

        for color in color_id:
            for i in color_id[color]:

                x.append(i[0])
                y.append(i[1])
                color_lable.append(color)

        plt.scatter(x, y, c=color_lable,
                    marker=',', lw=0, s=1, cmap='plasma')
        plt.savefig('demo-{}.jpg'.format(time.time()), dpi=100)
        plt.show()

        print(_temp)


if __name__ == "__main__":
    DBSCAN = DBSCAN(eps=1, minpts=5)
    img = DBSCAN.read_img("Demo2.bmp")
    DBSCAN.dbscan_preprocess(img)
    DBSCAN.dbscan()
