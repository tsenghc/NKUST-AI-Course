from reverse_board import Reverse_Board
import random
import copy


class Reverse_Game:
    def __init__(self):
        self.board = Reverse_Board()
        self.now_player = None

    def human_player(self, color):
        pass

    def change_player(self):
        if self.now_player is None:
            self.now_player = "●"
        else:
            if self.now_player == "●":
                self.now_player = "○"
            else:
                self.now_player = "●"

    def get_candidate_score(self, candidate):
        score = {}
        self.origin_board_status = copy.deepcopy(self.board.board)
        for p in candidate:
            self.board.put(p, self.now_player)
            board_score = alpha_beta(
                self.board.board).board_score(self.now_player)
            score[p] = board_score
        self.board.board = self.origin_board_status
        return score

    def second_candidate_score(self, candidate):
        score = {}
        first_candidtate = self.get_candidate_score(candidate)
        change = "○" if self.now_player == "●" else "●"

        for p in first_candidtate:
            self.board.put(p, self.now_player)
            rival_candidate = self.board.get_chess_position(change)
            self.second_board = self.board.board
            self.board.put(random.choice(rival_candidate), change)
            second_candidate = self.board.get_chess_position(self.now_player)
            for p2 in second_candidate:
                self.board.put(p, self.now_player)
                board_score = alpha_beta(
                    self.board.board).board_score(self.now_player)
                score[p] = {p2: board_score}
                self.board.board = self.second_board
        print(max(score))
        # _temp = []
        # for first in score:
        #     for second in first:
        #         _temp.append(second)
        self.board.board = self.origin_board_status
        return score

    def run(self):
        random_player = "○"
        winner = []
        for i in range(100):
            while True:
                game.change_player()
                candidate = (self.board.get_chess_position(self.now_player))
                # print(self.now_player, "可以下的位子(row,col)", candidate)
                if not any(candidate):
                    break

                if self.now_player == random_player:
                    self.board.put(random.choice(candidate), self.now_player)
                else:
                    evaluate_score = self.get_candidate_score(candidate)
                    max_score_position = candidate[list(evaluate_score.values()).index(
                        max(evaluate_score.values()))]
                    print(self.now_player, evaluate_score, max_score_position)
                    self.board.put(max_score_position, self.now_player)

                # self.board.display()
                # print(self.board.get_winner())
            winner.append(self.board.get_winner()[0])
            self.board = Reverse_Board()
        print('●:{}  ○:{}'.format(winner.count('●'), winner.count('○')))


class alpha_beta():
    def __init__(self, board_status) -> None:
        self.board = Reverse_Board()
        self.board_status = board_status
        self.square_weights = [
            [120, -20, 20, 5, 5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20, 5, 5, 20, -20, 120]
        ]

    def board_score(self, color_index):
        scores = {'●': 0, '○': 0}
        for x in range(8):
            for y in range(8):
                color_index = self.board_status[x][y]
                if color_index in scores:
                    scores[color_index] += self.square_weights[x][y]
        if color_index == "●":
            return scores['●']-scores['○']
        else:
            return scores['○']-scores['●']

    def max_node(self, alpha, beta, height, color):
        best_score = alpha
        best_move = (-1, -1)
        if height <= 0:
            best_score = self.board_score(color)
            return best_score
        elif not self.board.get_chess_position(color):
            color = '●' if color == '○' else '○'
            best_score = self.min_node(alpha, beta, height-1, color)
            return best_score

        candidate = (self.board.get_chess_position(self.now_player))
        max = alpha
        for move in candidate:
            color = '●' if color == '○' else '○'
            score = self.min_node(max, beta, height-1, color)
            self.board

    def min_node(self,  alpha, beta, height, color):
        best_score = beta
        if height <= 0:
            best_score = self.board_score(color)
            return best_score
        elif not self.board.get_chess_position(color):
            color = '●' if color == '○' else '○'
            best_score = self.max_node(alpha, beta, height-1, color)
            return best_score


if __name__ == '__main__':
    game = Reverse_Game()
    game.run()
