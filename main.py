import pygame
import os
from ai import *

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption('Tic Tac Toe AI')
screen = pygame.display.set_mode((DIM, DIM))

board = np.array([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']])


def draw_grid():
    pygame.draw.line(screen, BLACK, (DIM // 3, 0), (DIM // 3, DIM), 3)
    pygame.draw.line(screen, BLACK, (2 * DIM // 3, 0), (2 * DIM // 3, DIM), 3)
    pygame.draw.line(screen, BLACK, (0, DIM // 3), (DIM, DIM // 3), 3)
    pygame.draw.line(screen, BLACK, (0, 2 * DIM // 3), (DIM, 2 * DIM // 3), 3)


def draw_text(size, text, colour, x, y):
    font = pygame.font.SysFont('Comic Sans MS', size)
    text_surface = font.render(text, 1, colour)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def draw_board():
    for i in range(3):
        for j in range(3):
            draw_text(80, board[i, j], BLACK, j * DIM // 3 + DIM // 6, i * DIM // 3 + DIM // 6)


def update():
    global playing
    global win_line
    if check_win(board, 'X')[0]:
        playing = False
        win_line = check_win(board, 'X')[1:]

    elif check_win(board, 'O')[0]:
        playing = False
        win_line = check_win(board, 'O')[1:]

    elif check_draw(board):
        playing = False


playing = True
turn = 'X'
win_line = [(0, 0), (0, 0)]
start = True

while True:
    screen.fill(WHITE)
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT and playing and turn == PLAYERS[-1]:
                mouse = pygame.mouse.get_pos()
                pos = [mouse[1] // (DIM // 3), mouse[0] // (DIM // 3)]
                if space_free(board, pos):
                    place_marker(board, turn, pos)
                    turn = PLAYERS[1]
                    update()
            elif event.button == pygame.BUTTON_RIGHT and not playing:
                board = reset()
                playing = True
                turn = 'X'
                win_line = [(0, 0), (0, 0)]
                PLAYERS[1] = change(PLAYERS[1])
                PLAYERS[-1] = change(PLAYERS[-1])

    if playing and turn == PLAYERS[1]:
        begin = process_time()
        move = negamax_ab_with_memory(board, 1, -math.inf, math.inf)[0]
        place_marker(board, PLAYERS[1], move)
        turn = PLAYERS[-1]
        finish = process_time()
        update()

    draw_board()
    if not playing:
        pygame.draw.line(screen, BLACK, win_line[0], win_line[1], 7)
    pygame.display.flip()
