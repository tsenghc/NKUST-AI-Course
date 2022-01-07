class Reverse_Board:
    def __init__(self):
        self.empty = '.'
        self.board = [[self.empty for _ in range(
            8)] for _ in range(8)]
        self.board[3][4], self.board[4][3] = '●', '●'
        self.board[3][3], self.board[4][4] = '○', '○'
        self.direction = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                          (1, 0), (1, -1), (0, -1), (-1, -1)]

    def display(self):
        board = self.board
        print(' ', ' '.join(list('01234567')))
        for i in range(8):
            print(str(i), ' '.join(board[i]))

    def check_in_board(self, col, row):
        return row >= 0 and row <= 7 and col >= 0 and col <= 7

    def put(self, position, color):
        """[放置棋子，如果位子合法就反轉，沒有能反轉的回傳false]
        """
        fliped = self.can_fliped(position, color)
        if fliped:
            for flip in fliped:
                col, row = flip
                self.board[col][row] = color

            col, row = position
            self.board[col][row] = color
            return fliped
        else:
            return False

    def can_fliped(self, position, color):
        """[確定這裡能不能下，能下就回傳需要被反轉的棋子]
        """
        flipped_rival_chess = []
        new_x, new_y = position
        if not self.check_in_board(new_x, new_y) or\
                self.board[new_x][new_y] != self.empty:
            return False

        self.board[new_x][new_y] = color
        rival_color = "○" if color == "●" else "●"

        for x_direct, y_direct in self.direction:
            x, y = new_x+x_direct, new_y+y_direct
            if self.check_in_board(x, y) and\
                    self.board[x][y] == rival_color:
                x += x_direct
                y += y_direct
                if not self.check_in_board(x, y):
                    continue

                while self.board[x][y] == rival_color:
                    x += x_direct
                    y += y_direct
                    if not self.check_in_board(x, y):
                        break
                if not self.check_in_board(x, y):
                    continue

                if self.board[x][y] == color:
                    while True:
                        x -= x_direct
                        y -= y_direct
                        if x == new_x and y == new_y:
                            break
                        flipped_rival_chess.append([x, y])

        self.board[new_x][new_y] = self.empty  # reset board

        if len(flipped_rival_chess) == 0:
            return False

        return flipped_rival_chess

    def get_chess_position(self, color):
        """[找到對手棋子附近的空位，並驗證是否可以落子]
        """
        rival_color = "○" if color == "●" else "●"
        rival_color_points = []

        board = self.board
        for i in range(8):
            for j in range(8):
                if board[i][j] == rival_color:
                    for dx, dy in self.direction:
                        row, col = i + dx, j + dy
                        if self.check_in_board(col, row) and\
                                board[row][col] == self.empty and\
                                (row, col) not in rival_color_points:
                            rival_color_points.append((row, col))

        can_fliped_point = []
        for p in rival_color_points:
            if self.can_fliped(p, color):
                can_fliped_point.append(p)
        return can_fliped_point

    def get_winner(self):
        black_count, white_count = 0, 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == '●':
                    black_count += 1
                if self.board[i][j] == '○':
                    white_count += 1
        if black_count > white_count:
            return '●', black_count - white_count
        elif black_count < white_count:
            return '○', white_count - black_count
        elif black_count == white_count:
            return "平"


if __name__ == '__main__':
    # '●' '○'
    board = Reverse_Board()

    board.display()
    print(list(board.get_chess_position('○')))
    board.put((3, 5), "○")
    board.display()
    print(list(board.get_chess_position('●')))
    board.put((2, 5), "●")
    board.display()
    print(board.get_winner())
