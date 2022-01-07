def solveNQueens(n):
    def DFS(queens, xy_dif, xy_sum):
        p = len(queens)
        if p == n:
            result.append(queens)
            return None
        for q in range(n):
            if q not in queens and p-q not in xy_dif and p+q not in xy_sum:
                DFS(queens+[q], xy_dif+[p-q], xy_sum+[p+q])
    result = []
    DFS([], [], [])
    return result


def getCollisionNum(board):
    num = 0
    coll_list = []
    for col in range(len(board)):
        for anotherCol in range(col+1, len(board)):
            if board[col] == board[anotherCol]:
                num += 1  # collied in the same row
                coll_list.append([col, anotherCol])
            elif abs(board[col] - board[anotherCol]) == (anotherCol - col):
                num += 1  # collied diagonally
                coll_list.append([col, anotherCol])
    # print(coll_list)
    return num


curr_board = solveNQueens(8)
for i in curr_board:
    print(getCollisionNum(i))
