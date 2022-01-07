from PIL import Image
import numpy as np
from sklearn import datasets
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from tqdm import tqdm
import cv2


def scan(data, tree, labels, pid, cluster_id,
         eps, min_pts, visited_ist, neighbor_stack):  # 以此中心進行掃描

    neighbor_list = []
    neighbor_list = tree.query_ball_point(data[pid], eps)
    neighbor_list.remove(pid)
    print(len(neighbor_list))
    if len(neighbor_list) > min_pts:  # 掃到的點數量超過MinPts
        for i in neighbor_list:
            labels[i] = cluster_id  # 掃描到的點予以上色分群
            # 逐一檢查掃描到的點是不是新點，如果是的話append到stack裡等等在DBSCAN主函式以stack pop掃描
            if i not in neighbor_stack and i not in visited_ist:
                neighbor_stack.append(i)

        # 看看Stack空了沒，空了代表群分完了，return給主函式知道，ClustersId+1
        if not neighbor_stack:
            return True

    else:  # 掃到的點數量沒有超過MinPts
        
        labels[pid] = False  # 雜訊


def min_distance(point, data, eps):
    distance_1d = np.power(np.subtract(
        point, data, dtype=np.float32), 2).sum(axis=1)
    distance_1d = np.power(distance_1d, 0.5)
    min_distance = np.where(distance_1d <= eps)[0]
    return min_distance


def DBSCAN(data, eps, min_pts):
    progress = tqdm(total=len(data))
    labels = [False]*len(data)  # 建立每一點的歸類群列表label
    tree = KDTree(data)
    cluster_id = 1
    visited_list = []  # 未遍歷名單
    neighbor_stack = []  # 單群內關聯Stack
    pair_point_list = []
    p_id = 0

    # for point in tqdm(data):
    #     min_distance_list = min_distance(point, data, eps)
    #     pair_point_list.append(min_distance_list)

    while len(visited_list) != len(data):  # 迴圈直到遍歷所有資料點
        if neighbor_stack:  # 如果stack有東西，pop出來掃描，反之使用i掃描
            stack_pid = neighbor_stack.pop()  # Stack pop
            # pop出來的東西掃描，同時檢查Stack，檢查在scan函式內，return一個boolean來決定ClustersId
            if scan(data, tree, labels, stack_pid, cluster_id, eps, min_pts, visited_list, neighbor_stack):
                cluster_id = cluster_id+1
            visited_list.append(stack_pid)  # pop出來的Pid加入已遍歷名單
            progress.update(1)
        else:
            if p_id in visited_list:  # 如果中心點先被stack拿去掃了，跳出本次迴圈，否則正常使用Pid掃描
                p_id = p_id+1
                continue
            else:
                if scan(data, tree, labels, p_id, cluster_id, eps, min_pts, visited_list, neighbor_stack):  # Pid掃描後+1
                    cluster_id = cluster_id+1
                visited_list.append(p_id)  # pop出來的Pid加入已遍歷名單
                p_id = p_id+1
                progress.update(1)

    return labels


def read_img(file_path):
    img = cv2.imread(filename=file_path)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
    img_array = []
    print(img.shape)
    for i in range(0, img.shape[1]):
        for j in range(0, img.shape[0]):
            if img[j][i][0] == 0:
                img_array.append([j, i])

    img_array = np.array(img_array)

    return img_array


img_array = read_img('Demo2.bmp')
print(img_array)
labels = DBSCAN(img_array, eps=1, min_pts=5)



plt.figure()
plt.scatter(img_array[:, 0], img_array[:, 1], c=labels, cmap='plasma')
plt.savefig('Demo1-2.jpg', dpi=100)
plt.show()
