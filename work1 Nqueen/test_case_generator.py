import random


def generate(size=8):
    f = open("eightQueensTest.txt", "wb")
    testCaseCount = 1000
    board = ""
    while testCaseCount > 0:
        testCaseCount -= 1
        for col in range(size):
            board += str(random.randint(0, size-1)) + ' '
        board += str(random.randint(0, size-1)) + '\n'
    f.write(str.encode(board))
    f.close()


if __name__ == '__main__':
    generate(size=20)
