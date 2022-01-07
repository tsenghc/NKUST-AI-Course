import random
import numpy as np
import matplotlib.pyplot as plt


class GA_n_queen():
    def __init__(self, queen, population_count, mutation_probability) -> None:
        self.queen = queen
        self.max_collision = (queen*(queen-1))/2
        self.population = [GA_n_queen.random_chromosome(
            queen=self.queen) for _ in range(population_count)]
        self.generation = 0
        self.mutation_probability = mutation_probability
        self.non_collision = []
        self.max_fittens = []

    def random_chromosome(queen):
        return random.sample([i for i in range(queen)], queen)

    def get_collision_num(board):
        # 計算皇后衝突數
        num = 0
        coll_list = []
        for col in range(len(board)):
            for other_col in range(col+1, len(board)):
                if board[col] == board[other_col]:
                    num += 1  # collied in the same row
                    coll_list.append([col, other_col])
                elif abs(board[col] - board[other_col]) == (other_col - col):
                    num += 1  # collied diagonally
                    coll_list.append([col, other_col])
        # print(coll_list)
        return num

    def peek_chromosome(chromosome_probability):  # 挑選中獎基因
        p = np.array(chromosome_probability)
        index = np.random.choice(
            [i for i in range(len(chromosome_probability))],
            size=p.size, replace=False, p=p.ravel())
        return index.tolist()

    def reproduce(x, y):  # 隨機切一個點，交換兩者基因片段
        n = len(x)
        cut = random.randint(0, n - 1)
        return [x[0:cut] + y[cut:n], y[0:cut] + x[cut:n]]

    def mutate(x):  # 隨機挑一個點突變
        n = len(x)
        choice = random.randint(0, n - 1)
        num = random.randint(1, n)
        if num in x:
            num = random.randint(1, n)
        x[choice] = num
        # print("MUTATE", x)
        return x

    def fittens(self):
        _non_collision = []
        chromosome_probability = []
        for i in self.population:
            # 最大衝突-目前衝突=皇后彼此沒有的衝突的數量(越高越沒有衝突)
            _non_collision.append(
                self.max_collision - GA_n_queen.get_collision_num(i))
            # print(GA_n_queen.get_collision_num(i))
        for k, b in enumerate(self.population):
            chromosome_probability.append(
                _non_collision[k]/sum(_non_collision))
        self.non_collision = _non_collision
        self.max_fittens.append(max(_non_collision))
        # print(chromosome_probability)
        return chromosome_probability

    def n_queen(self):
        while True:
            # print(self.generation)
            self.generation += 1
            # print(self.population)
            chromosome_probability = GA_n_queen.fittens(self)
            print("generation:{},max fitten:{}".format(
                self.generation, max(self.non_collision)))

            if self.max_collision in self.non_collision:
                break
            # print(chromosome_probability)
            index = GA_n_queen.peek_chromosome(chromosome_probability)
            new_population = []
            for peek_index in range(0, len(index), 2):
                crossover = GA_n_queen.reproduce(
                    self.population[peek_index], self.population[peek_index+1])
                for chrom in crossover:
                    new_population.append(chrom)
            # print(new_population)
            for k, v in enumerate(new_population):
                if random.random() >= self.mutation_probability:  # 產生突變機率
                    new_population[k] = GA_n_queen.mutate(v)
            self.population = new_population

        print("generation:{},max fitten:{}".format(
            self.generation, max(self.non_collision)))
        GA_n_queen.print_board(self)

    def print_board(self):
        ans_board = []
        for k, v in enumerate(self.non_collision):
            if v == self.max_collision:
                ans_board.append(self.population[k])
        print("Find {} ANS:{}".format(len(ans_board), ans_board))
        for a_board in ans_board:
            print("===BOARD:{}===".format(a_board))
            board = []
            for x in range(self.queen):
                board.append(["x"] * self.queen)

            for i in range(self.queen):
                board[i][a_board[i]-1] = "Q"

            for row in board:
                print(" ".join(row))
        # plt.figure(figsize=(10, 6), dpi=100, linewidth=0.5)
        # plt.plot([k for k in range(self.generation)],
        #          self.max_fittens, 's-', color='b', label="cureve")
        # plt.show()


if __name__ == "__main__":
    n_queen = GA_n_queen(queen=10,
                         population_count=100,
                         mutation_probability=0.01)
    n_queen.n_queen()
