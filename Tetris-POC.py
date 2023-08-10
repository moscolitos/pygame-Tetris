
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 08:07:34 2023

@author: Mosco
"""

import pygame
import random

pygame.init()

# Colors and settings
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH, HEIGHT = 375, 500  # Extra space on the right for next shape preview
block_size = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Improved Mini Tetris")

# Updated shapes with all Tetrominoes
shapes = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1, 1],      # T shape
     [0, 1, 0]],
    [[1, 1, 0],      # L shape
     [0, 1, 1]],
    [[0, 1, 1],      # J shape
     [1, 1, 0]],
    [[0, 1, 1],      # S shape
     [1, 1, 0]],
    [[1, 1],         # O shape
     [1, 1]],
    [[1, 1, 1],      # Z shape
     [1, 0, 0]]
]

speed = 2            # Initial speed. Lower is slower.
speed_increase = 0.1 # The amount by which speed increases
score_threshold = 500 # Score after which speed increases

# Initialize the shapes
current_shape = random.choice(shapes)
next_shape = random.choice(shapes)


current_position = [0, 0]

next_shape = random.choice(shapes)

board = [[0 for _ in range(WIDTH // block_size)] for _ in range(HEIGHT // block_size)]


def rotate_shape(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
            for x in range(len(shape[0]) - 1, -1, -1) ]

def can_move(shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board_x = x + position[0]
                board_y = y + position[1]
                if board_x < 0 or board_x >= len(board[0]) or board_y >= len(board) or board[board_y][board_x]:
                    return False
    return True

def merge_shape(board, shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + position[1]][x + position[0]] = 1

def clear_lines(board):
    full_lines = [i for i, row in enumerate(board) if all(row)]
    for i in full_lines:
        del board[i]
        board.insert(0, [0 for _ in range(WIDTH // block_size)])
    return len(full_lines)

def draw_next_shape(shape):
    offset_x = WIDTH - 100  # X offset from the game board
    offset_y = 50           # Y offset from the top of the screen
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, BLUE, (offset_x + x * block_size, offset_y + y * block_size, block_size, block_size))
    label = pygame.font.SysFont('sans', 20).render('Next Shape:', True, (0, 0, 0))
    screen.blit(label, (offset_x, offset_y - 30))

clock = pygame.time.Clock()
score = 0

running = True

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and can_move(current_shape, [current_position[0] - 1, current_position[1]]):
                current_position[0] -= 1
            elif event.key == pygame.K_RIGHT and can_move(current_shape, [current_position[0] + 1, current_position[1]]):
                current_position[0] += 1
            elif event.key == pygame.K_DOWN:
                current_position[1] += 1
            elif event.key == pygame.K_UP:
                rotated = rotate_shape(current_shape)
                if can_move(rotated, current_position):
                    current_shape = rotated
    if score > score_threshold:
        speed += speed_increase
        score_threshold += 500

    if can_move(current_shape, [current_position[0], current_position[1] + 1]):
        current_position[1] += 1
    else:
        merge_shape(board, current_shape, current_position)
        score += clear_lines(board) * 100
        current_shape = next_shape
        next_shape = random.choice(shapes)
        current_position = [0, 0]
        if not can_move(current_shape, current_position):
            break

    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, RED, (x * block_size, y * block_size, block_size, block_size))

    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, BLUE, ((x + current_position[0]) * block_size, (y + current_position[1]) * block_size, block_size, block_size))

    score_text = pygame.font.SysFont('sans', 20).render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))


    # After drawing the current shape and board, draw the next shape:
    draw_next_shape(next_shape)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
