import itertools

import numpy as np
from numpy.core.numeric import identity
from numpy.lib.function_base import append
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
        old_C = []
        for k, v in enumerate(unique):
            if counts[k] >= self.minsup:
                old_C.append(unique[k])
            else:
                self.delet_itemset.add(unique[k])
        return (old_C)

    def scan(self, combin_list):
        _temp = []
        for combin in tqdm.tqdm(combin_list):
            ismember = [set(combin).issubset(row)
                        for row in self.dataset.tolist()]
            member_index = np.where(ismember)[0]
            if len(member_index) >= self.minsup:
                _temp.append(combin.tolist())
            else:
                combin = combin.tolist()
                self.delet_itemset.append(combin)

        return _temp

    def num_list(self, L_table):
        num_list = []
        for k in tqdm.tqdm(L_table):
            if isinstance(k, np.int32):
                if k not in self.dataset:
                    num_list.append(k)
            else:
                for m in k:
                    if m not in self.dataset:
                        num_list.append(m)
        return list(set(num_list))

    def combin_filter(self, combin_list):
        print("combin_filter START")
        if not self.delet_itemset:
            return combin_list
        _temp = []
        del_list = []
        for del_item in tqdm.tqdm(self.delet_itemset):
            if del_item in del_list:
                continue

            if isinstance(del_item, tuple):
                ismember = [set(del_item).issubset(combin)
                            for combin in combin_list]
                member_index = np.where(ismember)[0]
                if member_index.size != 0:
                    _temp.append(member_index)

        del_list = np.unique(np.ravel(_temp))

        combin_index = np.setdiff1d(range(len(combin_list)), del_list)
        combin_out = []
        for i in combin_index:
            combin_out.append(combin_list[i])
        print("combin_filter DONE")
        return combin_out

    def apriori(self, dataset):
        old_L = Association_rules_Apriori.L1_count_item(
            self, dataset)[1::]  # 從一之後開始是為了去除補-1
        i = 1
        frq_items = 0
        print(i, "old_L", len(old_L))

        while True:
            i += 1
            frq_items += len(old_L)
            print("delet_itemset", len(self.delet_itemset))
            num_list = (np.union1d(
                old_L, np.setdiff1d(old_L, self.delet_itemset)))
            print("num_list", len(num_list))
            combin_list = np.array(
                [j for j in itertools.combinations(num_list, i)])
            print("BFcombin_list", len(combin_list))
            # combin_list = Association_rules_Apriori.combin_filter(
            #     self, combin_list)
            print("AFcombin_list", len(combin_list))
            self.delet_itemset = []
            old_L = Association_rules_Apriori.scan(self, combin_list)
            print(i, "old_L", len(old_L))
            if not old_L:
                print("NON")
                frq_items += len(old_L)
                print(frq_items)
                break
            elif len(old_L) <= self.minsup:
                frq_items += len(old_L)
                print("FINAL")
                print(frq_items)
                print(old_L)
                break

        print(frq_items)
        pass


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
        except identity:
            dataset_size = dataset_size-1
            break

    ds = np.reshape(ds, (dataset_size, longest_data))
    return ds


def load_NP_txt(file_path):
    ds = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        raw_data_list = str(f.read()).replace(
            "[", "").replace("]", "").replace("'", "")
        raw_data_list = raw_data_list.split('\n')

    for tid in raw_data_list:
        _temp = tid.split(',')
        if len(_temp) > 1:
            t_list = [int(i) for i in _temp]
            ds.append(t_list)

    return ds


if __name__ == '__main__':
    ara = Association_rules_Apriori(minsup=5.0)
    # dataset = load_NP_txt("min.txt")

    # t = timeit.timeit(stmt="load_data('T15I7N0.5KD1K.txt')",
    #                   setup="from __main__ import load_data", number=1)
    # print(t)
    # dataset = load_data("mini.txt")
    dataset = load_data("T15I7N0.5KD1K.txt")
    ara.apriori(dataset)
