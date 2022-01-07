import copy
from hashlib import new
import itertools

import numpy as np
import tqdm
from numba import jit
import timeit


class Association_rules_Apriori:
    def __init__(self, minsup) -> None:
        self.dataset = []
        self.minsup = minsup
        self.delet_itemset = set()
        self.num = 0

    def L1_count_item(self, dataset):
        self.dataset = dataset
        old_C = {}
        for items in tqdm.tqdm(self.dataset):
            for item in items:
                if item in old_C:
                    old_C[item] += 1
                else:
                    old_C[item] = 1
        self.num = len(old_C)
        old_L = Association_rules_Apriori.sup_filter(self, old_C)
        # print("C1", old_C, len(old_C))
        # print("L1", old_L, len(old_L))
        return dict(old_L)

    def sup_filter(self, C_table: dict):
        old_C = copy.deepcopy(C_table)
        for k, v in tqdm.tqdm(C_table.items()):
            if v < self.minsup:
                del old_C[k]
                self.delet_itemset.add(k)
        return old_C

    def scan(self, C_table, combin_list):
        old_C = {}
        print("SCAN START")
        for items in tqdm.tqdm(self.dataset):
            for combin in combin_list:
                if set(combin).issubset(items):
                    if combin in old_C:
                        old_C[combin] += 1
                    else:
                        old_C[combin] = 1

        return old_C

    def combin_filter(self, combin_list):
        del_index = set()
        print("combin_filter START")
        for k, combin in enumerate(tqdm.tqdm(combin_list)):
            for del_combin in self.delet_itemset:
                if isinstance(del_combin, tuple):
                    if set(del_combin).issubset(combin):
                        del_index.add(k)
                        continue
                else:
                    if del_combin in combin:
                        del_index.add(k)
                        continue
        _temp = []
        print("del_index", len(del_index))
        for i in tqdm.tqdm(range(len(combin_list))):
            if i not in del_index:
                _temp.append(combin_list[i])
        combin_list = copy.deepcopy(_temp)
        return combin_list

    def num_list(self, L_table):
        num_list = []
        for k in tqdm.tqdm(L_table.keys()):
            if isinstance(k, int):
                if k not in self.dataset:
                    num_list.append(k)
            else:
                for m in k:
                    if m not in self.dataset:
                        num_list.append(m)
        return list(set(num_list))

    def np_combin_filter(self, combin_list):
        np_combin = []
        for k in combin_list:
            np_combin.append(list(k))
        np_combin = np.array(np_combin)

        np_delete_itemlist = []
        for i in self.delet_itemset:
            if isinstance(i, tuple):
                _mm = list(i)
                np_delete_itemlist.append(_mm)
            else:
                np_delete_itemlist.append(i)
        np_delete_itemlist = np.array(np_delete_itemlist)

        print("np_combin", np_combin)
        print("np_delete_itemlist", np_delete_itemlist)
        new_combin = np_combin-np_delete_itemlist
        print(new_combin)
        # print("np_delete_itemset", len(np_combin),
        #       len(np_delete_itemset), new_combin)

    def apriori(self, dataset):
        old_L = {}
        old_L = Association_rules_Apriori.L1_count_item(self, dataset)
        frq_items = 0
        i = 1
        print(i, "old_L", (old_L))
        while True:
            i += 1
            frq_items += len(old_L)

            print("delet_itemset", len(self.delet_itemset))

            num_list = Association_rules_Apriori.num_list(self, old_L)
            print("num_list", num_list[0:10], len(num_list))

            combin_list = [j for j in itertools.combinations(num_list, i)]
            print("BFcombin_list", combin_list[0:10], len(combin_list))
            # combin_list = Association_rules_Apriori.combin_filter(
            #     self, combin_list)
            print("AFcombin_list", combin_list[0:10], len(combin_list))
            old_C = Association_rules_Apriori.scan(self, old_L, combin_list)
            print(i, "old_C", len(old_C))
            old_L = Association_rules_Apriori.sup_filter(self, old_C)
            print(i, "old_L", len(old_L))
            if not old_L:
                print("NON OLDL")
                frq_items += len(old_C)
                print("old_C", old_C, len(old_C))
                break
            else:
                if sum(old_L.values())/len(old_L) <= self.minsup \
                        or len(old_L) == 1:
                    print(sum(old_L.values()), len(old_L))
                    frq_items += len(old_L)
                    print("FINAL", old_L)
                    break

        print(frq_items)


def load_data(file_path):
    ds = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        raw_data_list = f.read().split('\n')
    for tid in raw_data_list:
        _temp = tid.split(',')
        t_list = [int(i) for i in _temp]
        ds.append(t_list)

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
    ara = Association_rules_Apriori(minsup=2.0)
    # t = timeit.timeit(stmt="load_data('T15I7N0.5KD1K.txt')",
    #                   setup="from __main__ import load_data", number=1)
    # print(t)
    # dataset = load_NP_txt("min.txt")
    dataset = load_data("mini.txt")
    # dataset = load_data("T15I7N0.5KD1K.txt")
    # print(len(dataset))
    ara.apriori(dataset)
