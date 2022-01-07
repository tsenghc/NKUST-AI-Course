from datetime import date
import numpy as np
import tqdm


class Association_rules_Apriori:
    def __init__(self, minsup) -> None:
        self.dataset = None
        self.minsup = minsup
        self.delet_itemset = []
        self.num = 0

    def L1_count_item(self, dataset):
        self.dataset = dataset
        print(self.dataset.shape)
        unique, counts = np.unique(self.dataset, return_counts=True)
        old_C = {}
        for i in tqdm.tqdm(unique):
            t_id = np.where(self.dataset == i)[0]
            if not old_C.get(i):
                old_C[i] = list()
                old_C[i].append(t_id)
            else:
                old_C[i].append(t_id)
        del old_C[-1]
        old_L = {}
        for k, v in old_C.items():
            if (v[0].shape[0]) >= self.minsup:
                old_L[k] = v[0]

        return old_L

    def apriori(self, dataset):
        old_L = Association_rules_Apriori.L1_count_item(
            self, dataset)
        count = 1
        frq_items = len(old_L)
        print("L{}:{}".format(count, frq_items))
        while True:
            count += 1
            old_L_index = list(old_L.keys())
            _temp = {}
            for k in tqdm.tqdm(range(len(old_L_index))):
                for m in range(k+1, len(old_L_index)):
                    if count > 2:
                        if not any([old_L_index[k][:-1] == old_L_index[m][:-1]]):
                            break
                    intersection = np.intersect1d(
                        old_L[old_L_index[k]], old_L[old_L_index[m]])
                    # 交集的數量>=minsup
                    if intersection.size >= self.minsup:
                        item_combin = np.unique(
                            [old_L_index[k], old_L_index[m]])
                        _temp[tuple(item_combin)] = list(intersection)
            old_L = _temp
            frq_items += len(old_L)
            print("L{}:{}".format(count, len(old_L)))
            if not old_L:
                break
            elif len(old_L) <= self.minsup:
                break
        print("Done frq item:{}".format(frq_items))


def load_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        raw_data_list = f.read().split('\n')
    longest_data = max([len(i.split(",")) for i in raw_data_list])
    dataset_size = len(raw_data_list)
    ds = []
    for tid in tqdm.tqdm(raw_data_list):
        _temp = tid.split(',')
        try:
            t_list = [int(i) for i in _temp]
            _row = np.pad(t_list, (0, longest_data-len(_temp)),
                          'constant', constant_values=(-1))
            ds.append(_row)
        except ValueError:
            print(_temp[0])
            dataset_size = dataset_size-1
            break

    ds = np.reshape(ds, (dataset_size, longest_data))
    return ds


if __name__ == '__main__':
    import timeit
    apriori_dataset = {
        "T10I10N0.1KD1K": 4.0,
        "T20I15N1KD10K": 9.0,
        "T12I30N0.5KD100K": 300.0,
        "T18I20N2KD5000K": 65000.0
    }
    for data in apriori_dataset.keys():
        ara = Association_rules_Apriori(minsup=apriori_dataset[data])
        print("RUN {}".format(data))
        t = timeit.timeit(stmt="ara.apriori(load_data('{}.txt'))".format(data),
                          setup="from __main__ import ara,load_data", number=1)
        print(data, "TIME_COSTS/s:", t)
