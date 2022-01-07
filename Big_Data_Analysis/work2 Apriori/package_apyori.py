
from apyori import apriori


def load_data(file_path):
    ds = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        raw_data_list = f.read().split('\n')
    for tid in raw_data_list:
        _temp = tid.split(',')
        t_list = [int(i) for i in _temp]
        ds.append(t_list)

    return ds


if __name__ == '__main__':

    dataset = load_data("mini.txt")
    # dataset = load_data("T15I7N0.5KD1K.txt")

    association_rules = apriori(
        dataset, min_support=0.005)
    association_results = list(association_rules)
    print(association_results[8])
