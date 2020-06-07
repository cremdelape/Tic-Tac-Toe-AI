import numpy as np
from conf import *


def space_free(board, pos):
    return board[pos[0], pos[1]] == ' '


def check_win(board, marker):
    # Check Rows
    for i in range(3):
        if list(board[i, :]) == [marker] * 3:
            start = (DIM // 6, i * DIM // 3 + DIM // 6)
            end = (2 * DIM // 3 + DIM // 6, i * DIM // 3 + DIM // 6)
            return [True, start, end]

    # Check Columns
    for j in range(3):
        if list(board[:, j]) == [marker] * 3:
            start = (j * DIM // 3 + DIM // 6, DIM // 6)
            end = (j * DIM // 3 + DIM // 6, 2 * DIM // 3 + DIM // 6)

            return [True, start, end]

    # Check Diagonals
    if list(board.diagonal()) == [marker] * 3:
        start = (DIM // 6, DIM // 6)
        end = (2 * DIM // 3 + DIM // 6, 2 * DIM // 3 + DIM // 6)
        return [True, start, end]
    if list(np.fliplr(board).diagonal()) == [marker] * 3:
        start = (DIM // 6, 2 * DIM // 3 + DIM // 6)
        end = (2 * DIM // 3 + DIM // 6, DIM // 6)
        return [True, start, end]

    return [False, None, None]


def check_draw(board):
    return ' ' not in board


def place_marker(board, marker, pos):
    board[pos[0], pos[1]] = marker


def change(marker):
    if marker == 'X':
        marker = 'O'
    else:
        marker = 'X'
    return marker


def reset():
    board = np.array([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']])
    return board
