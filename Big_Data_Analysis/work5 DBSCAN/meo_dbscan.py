from PIL import Image, ImageOps
import numpy as np
from sklearn import datasets
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys
import cv2


class dbscan:
    def __init__(self, data, eps, minpts) -> None:
        self.eps = eps
        self.minpts = minpts
        self.data = data
        self.stack = []
        self.visited_list = []
        self.color_list = [False]*len(data)
        self.cid = 1
        self.tree = KDTree(data)
        self.neighbor_list = []

    def scan(self, pid):  # 以此中心進行掃描

        NeighborC = []
        NeighborC = self.tree.query_ball_point(
            self.data[pid], self.eps)  # 記錄掃描到的點
        NeighborC.remove(pid)

        if len(NeighborC) >= self.minpts:  # 掃到的點數量超過MinPts
            for i in NeighborC:  # 逐一檢查掃描到的點是不是新點，如果是的話append到stack裡等等以stack pop掃描
                self.color_list[i] = self.cid  # 掃描到的點予以上色分群
                if i not in self.stack and i not in self.visited_list:
                    self.stack.append(i)

            # 看看Stack空了沒，空了代表群分完了，return給主函式知道，cid+1
            if not self.stack:
                return True
            else:
                return False

        else:  # 掃到的點數量沒有超過MinPts
            self.color_list[pid] = False  # 雜訊
            return False

    def min_distance(self, point):
        distance_1d = np.power(np.subtract(
            point, self.data, dtype=np.float32), 2).sum(axis=1)
        distance_1d = np.power(distance_1d, 0.5)
        min_distance = np.where(distance_1d <= self.eps)[0]
        return min_distance

    def fit(self):
        pid = 0
        progress = tqdm(total=len(self.data))

        # for i in tqdm(self.data):
        #   min_distance = self.min_distance(i)
        #   self.neighbor_list.append(min_distance)

        while len(self.visited_list) != len(self.data):  # 迴圈直到遍歷所有資料點
            if self.stack:  # 如果stack有東西，pop出來掃描，反之使用i掃描
                stack_pid = self.stack.pop()  # Stack pop
                if self.scan(stack_pid):  # pop出來的東西掃描，同時檢查Stack
                    self.cid = self.cid+1
                self.visited_list.append(stack_pid)  # pop出來的pid加入已遍歷名單
                progress.update(1)
            else:
                if pid in self.visited_list:  # 如果點先被stack拿去掃了，跳出本次迴圈，否則正常使用pid掃描
                    pid = pid+1
                    continue
                else:
                    if self.scan(pid):  # pid掃描後+1
                        self.cid = self.cid+1
                    self.visited_list.append(pid)
                    pid = pid+1
                progress.update(1)

        self.data = np.array([self.data[k] for k, v in enumerate(
            self.color_list) if self.color_list[k] != False])
        # for k 為 index，ColorList的所有index 對應到ColorList如果不為False，以此作為data[k]生成新的list後轉np.array，此舉可以生成一個沒有noise的data
        self.color_list = [v for v in self.color_list if v != False]
        # for v 為 value，ColorList的所有value如果不為False(noise)，以此生成新的list後轉np.array，此舉可以生成一個沒有noise的ColorList

        return self.data, self.color_list, self.cid


def main(argv):

    img = cv2.imread(filename=argv[1])
    img_shape = img.shape

    img = img.reshape(-1, 3)[:, 0]

    point = np.where(img == 0)
    y_len = np.full(point[0].shape[0], img_shape[1], dtype=int)
    point_row_index = point//y_len
    point_col_index = point % y_len

    data = np.array(
        list(zip(point_col_index[0], point_row_index[0])), dtype=np.uint16)

    print("eps", int(argv[2]))
    DBSCAN = dbscan(data, int(argv[2])+1, int(argv[3]))
    data, labels, CCount = DBSCAN.fit()
    # print(X)
    # print(labels)
    plt.figure()
    plt.scatter(data[:, 0], data[:, 1], s=1, c=labels)
    plt.axis('equal')
    plt.title('Prediction')
    plt.show()
    print(argv[1], "_", int(argv[2]), "_", float(argv[2]))
    print("群數", CCount)


if __name__ == "__main__":
    main(sys.argv)
