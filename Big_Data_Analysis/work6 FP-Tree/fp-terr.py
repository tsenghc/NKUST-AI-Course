import numpy as np
import tqdm
import collections


class Association_rules_FP_tree:
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
        for k, v in enumerate(unique):
            if counts[k] >= self.minsup:
                old_C[v] = counts[k]
        del old_C[-1]
        old_L = dict(
            sorted(old_C.items(), key=lambda item: item[1], reverse=True))
        return old_L

    def sort_db(self, dataset):
        old_L = Association_rules_FP_tree.L1_count_item(self, dataset)
        new_db = []
        for transetion in tqdm.tqdm(dataset):
            _row = {}
            for shop in transetion:
                if old_L.get(shop):
                    _row[shop] = old_L[shop]
            _row = dict(
                sorted(_row.items(), key=lambda item: item[1], reverse=True))
            new_db.append(_row.keys())
        return new_db


class node:
    def __init__(self, val, char):
        self.val = val  # is used to define the current count
        # is used to define what the current character is.
        self.char = char
        self.children = {}  # for storing children
        self.next = None  # for linked lists, linked to another child
        self.father = None  # Search up when building a conditional tree
        # When using the linked list, observe if it has been visited.
        self.visit = 0
        self.nodelink = collections.defaultdict()
        self.nodelink1 = collections.defaultdict()


class FPTree():
    def __init__(self) -> None:
        self.root = node(-1, 'root')
        self.FrequentItem = collections.defaultdict(
            int)  # is used to store frequent itemsets
        self.res = []
        # Create a function of the fp tree, data should be in the form of list[list[]], where the internal list contains the name of the item, represented by a string

    def BuildTree(self, data):

        for line in data:  # take the first list, use line to represent
            root = self.root
            for item in line:  # for each item in the list

                if item not in root.children.keys():  # if item is not in dict
                    root.children[item] = node(
                        1, item)  # Create a new node
                    # is used to search from the bottom up
                    root.children[item].father = root
                else:
                    # Otherwise, count plus 1
                    root.children[item].val += 1
                    root = root.children[item]  # Go one step down

                    # Create a linked list based on this root
            if item in self.root.nodelink.keys():  # if this item already exists in nodelink
                if root.visit == 0:  # If this point has not been visited
                    self.root.nodelink1[item].next = root
                    self.root.nodelink1[item] = self.root.nodelink1[item].next
                    root.visit = 1  # was visited

                else:  # If this item does not exist in nodelink
                    self.root.nodelink[item] = root
                    self.root.nodelink1[item] = root
                    root.visit = 1
        print('tree build complete')
        return self.root


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


if __name__ == '__main__':
    fp_tree = Association_rules_FP_tree(minsup=5.0)
    dataset = load_data("T15I7N0.5KD1K.txt")
    db = fp_tree.sort_db(dataset)
    FP = FPTree()
    FP.BuildTree(db)
