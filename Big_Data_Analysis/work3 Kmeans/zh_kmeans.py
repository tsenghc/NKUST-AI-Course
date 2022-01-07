import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def kmeans(data, k=3, normalize=False, limit=500):
    # normalize 数据
    if normalize:
        stats = (data.mean(axis=0), data.std(axis=0))
        data = (data - stats[0]) / stats[1]

    # 直接将前K个数据当成簇中心
    centers = data[:k]

    for i in range(limit):
        # 首先利用广播机制计算每个样本到簇中心的距离，之后根据最小距离重新归类
        classifications = np.argmin(
            ((data[:, :, None] - centers.T[None, :, :])**2).sum(axis=1), axis=1)
        # 对每个新的簇计算簇中心
        new_centers = np.array(
            [data[classifications == j, :].mean(axis=0) for j in range(k)])

        # 簇中心不再移动的话，结束循环
        if (new_centers == centers).all():
            break
        else:
            centers = new_centers
    else:
        # 如果在for循环里正常结束，下面不会执行
        raise RuntimeError(
            f"Clustering algorithm did not complete within {limit} iterations")

    # 如果normalize了数据，簇中心会反向 scaled 到原来大小
    if normalize:
        centers = centers * stats[1] + stats[0]

    return classifications, centers


data = np.random.rand(200, 3)
classifications, centers = kmeans(data, k=3)
print(classifications, centers)


# plt.figure(figsize=(12, 8))
# plt.scatter(x=data[:, 0], y=data[:, 1], s=100, c=classifications)
# plt.scatter(x=centers[:, 0], y=centers[:, 1], s=500, c='k', marker='^')
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=classifications, s=100)
ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], s=500, c='k', marker='^');
plt.show()
