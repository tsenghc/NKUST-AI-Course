from fpgrowth_py import fpgrowth


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
    dataset = load_data("T15I7N0.5KD1K.txt")

    freqItemSet, rules = fpgrowth(dataset, minSupRatio=0.005, minConf=0.5)
    print(freqItemSet)
    print(rules)
# [[{'beer'}, {'rice'}, 0.6666666666666666], [{'rice'}, {'beer'}, 1.0]]
# rules[0] --> rules[1], confidence = rules[2]
