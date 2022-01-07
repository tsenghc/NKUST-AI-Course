import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import copy
from sklearn import datasets
import tqdm
import copy


class DBSCAN:
    def __init__(self, eps, minpts) -> None:
        self.eps = eps
        self.minpts = minpts
        self.dataset = None
        self.stack = []
        self.scaned = []
        self.color_id = 0

    def read_img(self, file_path) -> np.array:
        img = cv2.imread(filename=file_path)
        self.img_shape = img.shape

        return img

    def data_gen(self):
        X, y = datasets.make_blobs(n_samples=50, centers=3,
                                   n_features=2, random_state=20, cluster_std=1.5)
        self.dataset = X
        return X

    def dbscan_preprocess(self, img):
        img = img.reshape(-1, 3)[:, 0]
        background = np.where(img == 255)
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

    def scan(self, color_id, pair_point, point_index):

        _already_scan = []
        point_color = {}
        if pair_point.shape[0] >= self.minpts:
            for point in pair_point:  # 小的表
                point_color[point] = self.color_id
                if point not in self.stack and\
                        pair_point not in _already_scan:
                    self.stack.append(point)
            if not self.stack:
                return True
        else:
            point_color[point_index] = False
        return point_color

    def dbscan(self):
        pair_point_list = []
        _already_scan = []
        pid = 0

        for point in tqdm.tqdm(self.index_list):
            min_distance_list = DBSCAN.min_distance(point)
            pair_point_list.append(min_distance_list)

        while len(_already_scan) != len(pair_point_list):
            if self.stack:
                stack_point_id = self.stack.pop()

                _already_scan.append(stack_point_id)

            else:
                if p_id in visited_list:  # 如果中心點先被stack拿去掃了，跳出本次迴圈，否則正常使用Pid掃描
                    p_id = p_id+1
                    continue

                print(color_point)

        pass


if __name__ == "__main__":
    DBSCAN = DBSCAN(eps=1, minpts=5)
    img = DBSCAN.read_img("Demo2.bmp")
    # img = dbscan.data_gen()
    # dbscan.draw_img(img)
    DBSCAN.dbscan_preprocess(img)
    DBSCAN.dbscan()
