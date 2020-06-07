import math
from board import *
from conf import *


# The Transposition Table of form  {node:[[move, value], flag]}
# Node is the numpy array representing the state, the move is a tuple and flag represents whether the value is exact,
# lower or upper

TRANSPOSTION_TABLE = {}


def negamax_ab_with_memory(board, colour, alpha, beta):
    alpha_org = alpha
    # Transpostion tabel look up
    if board.tostring() in TRANSPOSTION_TABLE:
        tt_entry = TRANSPOSTION_TABLE[board.tostring()]
        if tt_entry[1] == 'EXACT':
            return tt_entry[0]
        elif tt_entry[1] == 'LOWERCASE':
            alpha = max(alpha, tt_entry[0][1])
        elif tt_entry[1] == 'UPPERCASE':
            beta = min(beta, tt_entry[0][1])

        if alpha >= beta:
            return tt_entry[0]

    # If Terminal Node then return evaluation
    if check_win(board, PLAYERS[1])[0]:
        best = [(-1, -1), colour * 10]
        return best

    elif check_win(board, PLAYERS[-1])[0]:
        best = [(-1, -1), colour * -10]
        return best

    elif check_draw(board):
        best = [(-1, -1), 0]
        return best

    best = [(-1, -1), -math.inf]
    cutoff = False

    # Loop through all child nodes
    for i in range(3):
        for j in range(3):
            # If the move is valid do
            pos = (i, j)
            if space_free(board, pos):
                place_marker(board, PLAYERS[colour], pos)
                score = -negamax_ab_with_memory(board, -colour, -beta, -alpha)[1]
                place_marker(board, ' ', pos)
                if score > best[1]:
                    best = [pos, score]
                alpha = max(alpha, best[1])
                # Cutoff
                if alpha >= beta:
                    cutoff = True
                    break
        if cutoff:
            break

    store(TRANSPOSTION_TABLE, board, alpha_org, beta, best)

    return best


def store(table, board, alpha, beta, best):
    if best[1] <= alpha:
        flag = 'UPPERCASE'
    elif best[1] >= beta:
        flag = 'LOWERCASE'
    else:
        flag = 'EXACT'

    table[board.tostring()] = [best, flag]
