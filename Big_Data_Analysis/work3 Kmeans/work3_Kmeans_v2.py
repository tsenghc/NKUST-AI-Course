import cv2
import numpy as np
import matplotlib.pyplot as plt


class K_means:
    def __init__(self, n_clusters, max_iter, random_seed) -> None:
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
        self.data = img.reshape(-1, 3)
        return img, img.shape

    def draw_img(self, img):
        plt.imshow(img)
        plt.show()

    def kmeans(self):
        for i in range(self.max_iter):
            index_R = (self.data[:, :, None])  # index R
            center_R = self.center_point.T[None, :, :]  # 轉置後各中心點的R
            distance = pow((index_R-center_R), 2)  # 座標距離平方
            sum_distance = distance.sum(axis=1)  # 把各中心點距離加總
            point_for_cluster = np.argmin(sum_distance, axis=1)  # 找出距離最近的中心點
            new_centers = np.array(
                [self.data[point_for_cluster == j, :].mean(
                    axis=0) for j in range(self.n_clusters)],
                dtype=np.int32)  # 將各群的點取平均數算出中心
            if (new_centers == self.center_point).all():
                break
            else:
                self.center_point = new_centers

        new_img = []
        for self.n_clusters in point_for_cluster:
            new_img.append(self.center_point[self.n_clusters])

        return new_img


def run(img_path, clust):
    for k in range(2, clust+1):
        KM = K_means(n_clusters=k, max_iter=100,
                     random_seed=111)
        raw_img, raw_img_shape = KM.read_img(img_path)
        new_img = KM.kmeans()
        new_img = np.reshape(new_img, (raw_img_shape[0], raw_img_shape[1], 3))
        plt.imsave("K{k}_{img}.jpg".format(
            img=img_path, k=k), new_img.astype(np.uint8))
        # KM.draw_img(new_img)


if __name__ == '__main__':
    run("image002.jpg", 5)
