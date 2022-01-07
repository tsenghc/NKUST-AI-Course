import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import cv2


def read_img(file_path) -> np.array:
    img = cv2.imread(filename=file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.array(img)
    data = img.reshape(
        img.shape[0]*img.shape[1], img.shape[2])
    return img


if __name__ == "__main__":
    kmeans = KMeans(n_clusters=3)
    raw_data = read_img("image002.jpg")
    kmeans.fit(raw_data)
    print(kmeans.cluster_centers_)
