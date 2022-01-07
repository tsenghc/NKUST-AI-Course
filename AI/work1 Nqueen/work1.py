import random

from tqdm import tqdm


def get_collision_num(board):
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


def hill_climbing(board):
    queen_count = len(board)
    before_status = get_collision_num(board)
    count = 0
    if before_status != 0:
        for k, v in enumerate(board):
            board_status = {}
            for i in range(queen_count):
                count += 1
                board[k] = i
                board_status[(k, i)] = get_collision_num(board)
            board_status = sorted(board_status.items(), key=lambda x: x[1])
            if (board_status[0][1]) != 0:
                board[board_status[0][0][0]] = board_status[0][0][1]
            else:
                board[board_status[0][0][0]] = board_status[0][0][1]
                print("\nSTEP:", count)
                return list(board)

    return list(board)


def read_test(file_path="eightQueensTest.txt"):
    with open(file_path, "r") as ins:
        board = []
        for line in ins:
            _temp = [int(i) for i in line.replace("\n", "").split(" ")]
            board.append(_temp)
    return list(board)


def gen_test_txt(size=8, sample=500):
    f = open("eightQueensTest.txt", "wb")
    testCaseCount = sample
    board = ""
    while testCaseCount > 0:
        testCaseCount -= 1
        for col in range(0, size-1):
            board += str(random.randint(0, size-1)) + ' '
        board += str(random.randint(0, size-1)) + '\n'
    f.write(str.encode(board))
    f.close()


def save_output(save_path, board):
    with open(save_path, 'w')as file:
        file.write("{}\n".format(len(board)))
        for k, v in enumerate(board):
            file.write("{},{}\n".format(k, v))


def gen_board(size, sample):
    board = []
    for c in range(sample):
        board.append(random.sample([i for i in range(size)], size))
    return list(board)


if __name__ == "__main__":
    # 爬山演算法球N皇后
    gen_test_txt(size=8, sample=50)
    raw_board = read_test("eightQueensTest.txt")
    raw_board_2 = read_test("eightQueensTest.txt")
    # raw_board = gen_board(20, 500)

    for i in tqdm(range(len(raw_board))):
        board_status = hill_climbing(raw_board[i])

        if get_collision_num(board_status) == 0:
            print("RAW:", raw_board_2[i], i)
            print("ANS:", board_status)
            save_output('output.txt', board_status)
            for k, v in enumerate(board_status):
                print("{},{}".format(k, v))
            break
