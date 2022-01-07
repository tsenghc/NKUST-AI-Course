def loadDataSet():
    ds = []
    with open('T15I7N0.5KD1K.txt', mode='r', encoding='utf-8') as f:
        raw_data_list = f.read().split('\n')
    for tid in raw_data_list:
        _temp = tid.split(',')
        t_list = [int(i) for i in _temp]
        ds.append(t_list)

    return ds

# 输入数据集
# 输出候选项集列表C1


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))  # 对C1中每个项构建一个不变集合

# 输入数据集，候选项集列表Ck，最小支持度
# 输出频繁项集列表Lk，Ck各项的支持度


def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

# 输入频繁项集列表Lk、项集元素个数
# 输出下一个候选项集Ck


def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])  # 集合的并
    return retList

# 输入数据集，候选项集Ck，最小支持度
# 输出所有频繁项集列表，各项的支持度


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))
    L1, supportData = scanD(D, C1, minSupport)  #
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)  # 将supK的键值对添加到supportData
        L.append(Lk)
        k += 1
    return L, supportData


if __name__ == '__main__':
    dadaset = loadDataSet()
    L, supportData = apriori(dadaset, minSupport=0.5)
    print(L)
    for k in supportData:
        print(k, supportData[k])
