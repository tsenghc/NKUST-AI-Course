class ab_pruning:
    def __init__(self, tree_hight, tree_branch) -> None:
        self.tree_hight = tree_hight
        self.tree_branch = tree_branch
        self.pruning_data = []
        self.visit_node = []

    def minimax(self, depth, node_index, maximizing_player,
                values, alpha, beta):
        if depth == self.tree_hight:
            return values[node_index]

        if maximizing_player:
            best = MIN
            for i in range(0, self.tree_branch):
                val = ab_pruning.minimax(
                    depth + 1, node_index * self.tree_branch + i,
                    False, values,
                    alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)

                # 判斷是否需剪Alpha枝
                if beta <= alpha:
                    if depth == self.tree_hight-1:
                        self.visit_node.append(val)

                    ab_pruning.pruning(i, depth, node_index, values)

                    break
                if depth == self.tree_hight-1:
                    self.visit_node.append(val)
            return best
        else:
            best = MAX
            for i in range(0, self.tree_branch):
                val = ab_pruning.minimax(
                    depth + 1, node_index * self.tree_branch + i,
                    True, values,
                    alpha, beta)
                best = min(best, val)
                beta = min(beta, best)

                # 判斷是否需剪Beta枝
                if beta <= alpha:
                    if depth == self.tree_hight-1:
                        self.visit_node.append(val)
                    ab_pruning.pruning(i, depth, node_index, values)

                    break
                if depth == self.tree_hight-1:
                    self.visit_node.append(val)
            return best

    def pruning(self, i, depth, node_index, values):
        if self.tree_hight-depth == 1:
            value = values[(node_index * self.tree_branch + i)+1:
                           ((node_index+1) * self.tree_branch)]
            if len(value):
                _position =\
                    ((node_index * self.tree_branch + i)+1) + \
                    sum([self.tree_branch **
                         i for i in range(self.tree_hight)])
                self.pruning_data.append([value, _position])
        else:
            _child = self.tree_branch**(self.tree_hight-depth)
            _index = (_child*node_index + self.tree_branch*(i+1))
            value = values[_index: _index +
                           self.tree_branch*(self.tree_branch-i-1)]
            _up_node = sum(
                [self.tree_branch ** i for i in range(
                    self.tree_hight)])+_child*node_index
            _position = [k for k in range(
                _up_node+self.tree_branch*(i+1),
                _up_node+self.tree_branch*(self.tree_branch-i))]
            if len(value):
                for k, v in enumerate(value):
                    self.pruning_data.append([v, _position[k]])


def load_data(file_name):

    with open(file_name, 'r', encoding='utf-8') as f:
        raw_data = f.read().split("\n")
    tree_branch = int(raw_data[0])
    tree_hight = int(raw_data[1])
    node_value = [int(i) for i in raw_data[2].split(",")]
    return tree_branch, tree_hight, node_value


def data_gen(low, high, branch, deep):
    import numpy as np
    np.random.seed(123)
    dataset = (np.random.randint(low, high, branch**deep).tolist())
    print("GEN_dataset", dataset)
    return branch, deep, dataset


# Driver Code
if __name__ == "__main__":
    MAX, MIN = 1000, -1000

    # branch, hight, values = (data_gen(-25, 5, 2, 3))
    branch, hight, values = load_data("test-5.txt")
    ab_pruning = ab_pruning(tree_hight=hight, tree_branch=branch)
    root = ab_pruning.minimax(0, 0, True, values, MIN, MAX)

    print("visit_node have", len(ab_pruning.visit_node), ab_pruning.visit_node)
    print("root", root)
    print("pruning_data have", len(
        ab_pruning.pruning_data), ab_pruning.pruning_data)
