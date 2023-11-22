import sys
import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

WIDTH = 500
HEIGHT = 500

BOARD_ROWS = 4
BOARD_COLS = 4

TILE_SIZE = WIDTH // BOARD_COLS

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')

img_grid = pygame.image.load('images/grid.png')
img_2 = pygame.image.load("images/2.png")
img_4 = pygame.image.load("images/4.png")
img_8 = pygame.image.load("images/8.png")
img_16 = pygame.image.load("images/16.png")
img_32 = pygame.image.load("images/32.png")
img_64 = pygame.image.load("images/64.png")
img_128 = pygame.image.load("images/128.png")
img_256 = pygame.image.load("images/256.png")
img_512 = pygame.image.load("images/512.png")
img_1024 = pygame.image.load("images/1024.png")
img_2048 = pygame.image.load("images/2048.png")
img_tile = [img_2, img_4, img_8, img_16, img_32, img_64, img_128, img_256, img_512, img_1024, img_2048]

def init_board():
    board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
    add_random(board)
    add_random(board)
    return board

def draw_board(board):
    win.blit(img_grid, (-10, -10))

    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            val = board[i][j]
            if val > 0:
                tile = img_tile[val // 2 - 1]
                win.blit(tile, (j * TILE_SIZE, i * TILE_SIZE))

def game_over(board):
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == 0 or (i > 0 and board[i][j] == board[i - 1][j]) or (j > 0 and board[i][j] == board[i][j - 1]):
                return False
    return True

def add_random(board):
    empty_cells = []
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == 0:
                empty_cells.append((i, j))

    if len(empty_cells) > 0:
        cell = random.choice(empty_cells)
        board[cell[0]][cell[1]] = 2 if random.random() < 0.9 else 4

def get_value(board, row, col):
    return board[row][col]

def update_board(board):
    has_changed = False
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS):
            val = get_value(board, row, col)
            if val > 0:
                if row > 0 and get_value(board, row - 1, col) == val:
                    board[row - 1][col] *= 2
                    board[row][col] = 0
                    has_changed = True
                elif col > 0 and get_value(board, row, col - 1) == val:
                    board[row][col - 1] *= 2
                    board[row][col] = 0
                    has_changed = True
    if has_changed:
        add_random(board)
    return has_changed

def handle_input(board):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        move(board, UP)
    if keys[pygame.K_DOWN]:
        move(board, DOWN)
    if keys[pygame.K_LEFT]:
        move(board, LEFT)
    if keys[pygame.K_RIGHT]:
        move(board, RIGHT)

def move(board, direction):
    if direction == UP:
        board[:] = zip(*board)
        update_board(board)
        board[:] = zip(*board)
    elif direction == DOWN:
        board[:] = zip(*board)
        board = [row[::-1] for row in board]
        update_board(board)
        board = [row[::-1] for row in board]
        board[:] = zip(*board)
    elif direction == LEFT:
        update_board(board)
    elif direction == RIGHT:
        board = [row[::-1] for row in board]
        update_board(board)

        for row in board:
            board.append(row[::-1])

def main():
    board = init_board()
    clock = pygame.time.Clock()
    while not game_over(board):
        win.fill(WHITE)
        draw_board(board)
        handle_input(board)
        pygame.display.flip()
        clock.tick(60)
    print('Game over!')

pygame.display.init()
main()
pygame.quit()
sys.exit()