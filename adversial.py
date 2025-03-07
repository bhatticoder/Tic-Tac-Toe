# Making Tic Tac Toe using adversarial search minimax theory
# Practice makes a man perfect
import sys
import pygame as pg
import numpy as np

pg.init()
# colors
White = (255,255,255)
Grey = (180,180,180)
Red = (255,0,0)
Green = (0,255,0)
Black = (0,0,0)
# constant things of board
width = 300
height = 300
line_width = 5
board_row = 3
board_col = 3
square_size = width // board_col
circle_rad = square_size // 3
circle_width = 5
cross_width = 5
# Displaying board
screen = pg.display.set_mode((width,height))
pg.display.set_caption('Tic Tac Toe')
screen.fill(Black)
#
board = np.zeros((board_row, board_col))

def draw_lines(color = White):
    for i in range(1, board_row):
        pg.draw.line(screen,color,(0,square_size*i),(width,square_size*i),line_width)
        pg.draw.line(screen,color,(square_size*i,0),(square_size*i,height),line_width)

def draw_fig(color=White):
    for rows in range(board_row):
        for cols in range(board_col):
            center_x = int(cols * square_size + square_size // 2)
            center_y = int(rows * square_size + square_size // 2)

            if board[rows][cols] == 1:
                pg.draw.circle(screen, color, (center_x, center_y), circle_rad, circle_width)
            elif board[rows][cols] == 2:
                offset = square_size // 4
                pg.draw.line(screen, color,
                             (center_x - offset, center_y - offset),
                             (center_x + offset, center_y + offset),
                             cross_width)
                pg.draw.line(screen, color,
                             (center_x + offset, center_y - offset),
                             (center_x - offset, center_y + offset),
                             cross_width)

def mark_square(rows,cols,players):
    board[rows][cols] = players

def available_square(rows,cols):
    return board[rows][cols] == 0

def is_board_full(check_board=board):
    for rows in range(board_row):
        for cols in range(board_col):
            if check_board[rows][cols] == 0:
                return False  # Board is not full
    return True  # Board is full

def check_win(players, check_board=board):
    for cols in range(board_col):
        if check_board[0][cols] == players and check_board[1][cols] == players and check_board[2][cols] == players:
            return True
    for rows in range(board_col):
        if check_board[rows][0] == players and check_board[rows][1] == players and check_board[rows][2] == players:
            return True
    if check_board[0][0] == players and check_board[1][1] == players and check_board[2][2] == players:
        return True
    if check_board[0][2] == players and check_board[1][1] == players and check_board[2][0] == players:
        return True
    return False

def minimax(minimax_board,depth,is_maximizing):
    if check_win(2,minimax_board):
        return float('inf')
    elif check_win(1,minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0
    if is_maximizing:
        best_score = -1000
        for rows in range(board_row):
            for cols in range(board_col):
                if minimax_board[rows][cols] == 0:
                    minimax_board[rows][cols] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[rows][cols] = 0
                    best_score = max(score,best_score)
        return best_score
    else:
        best_score = 1000
        for rows in range(board_row):
            for cols in range(board_col):
                if minimax_board[rows][cols] == 0:
                    minimax_board[rows][cols] = 1  # Corrected to simulate human's move
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[rows][cols] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -1000
    move = (-1,-1)
    for rows in range(board_row):
        for cols in range(board_col):
            if board[rows][cols] == 0:
                board[rows][cols] = 2
                score = minimax(board,0,False)
                board[rows][cols] = 0
                if score > best_score:
                    best_score = score
                    move = (rows,cols)
    if move != (-1,-1):
        mark_square(move[0],move[1],2)
        return True
    return False

def restart_game():
    screen.fill(Black)
    draw_lines()
    for rows in range(board_row):
        for cols in range(board_col):
            board[rows][cols] = 0

draw_lines()
player = 1
game_over = False
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            row = mouseY // square_size
            col = mouseX // square_size

            if available_square(row, col):
                mark_square(row, col, player)
                if check_win(player):
                    game_over = True
                player = 2  # Switch to AI player

                if not game_over:
                    # AI's turn
                    best_move()
                    if check_win(2):
                        game_over = True
                    player = 1  # Switch back to human player

                if is_board_full() and not check_win(1) and not check_win(2):
                    game_over = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:  # Fixed key check
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_fig()
    else:
        if check_win(1):
            draw_fig(Green)
            draw_lines(Green)
        elif check_win(2):
            draw_fig(Red)
            draw_lines(Red)
        else:
            draw_fig(Grey)
            draw_lines(Grey)
    pg.display.update()