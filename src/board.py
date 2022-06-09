import numpy as np
import random
import pygame
import sys
import math

ROWS = 6
COLUMNS = 7

# Colors for the graphics
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# ALl the graphics calculations
SCALE = 100  # unit is in pixels
width = COLUMNS * SCALE
height = (ROWS + 1) * SCALE
size = (width, height)
screen = pygame.display.set_mode(size)
RADIUS = int(SCALE/2 - 5)


# Turn values
PLAYER = 0
COMPUTER_PLAYER = 1

# Mark values
PLAYER_MARK = 1
COMPUTER_PLAYER_MARK = 2
AVAILABLE = 0


def makeboard():
    # Top most row is the 5th row
    board = np.zeros((ROWS, COLUMNS))  # make a matrix of 6 rows and 7 columns
    return board


def makemove(board, row, col, mark):
    board[row][col] = mark


def isavailable(board, col):  # Checks if the given column is available to make a move
    return board[ROWS - 1][col] == AVAILABLE  # If it is true then we are good to make a move in this column!


def getnextavailablerow(board, col):
    for row in range(ROWS):
        if board[row][col] == AVAILABLE:
            return row

def isTie(board):
    for col in range(COLUMNS):
        for row in range(ROWS):
            if board[row][col] == AVAILABLE:
                return False
    return True

def checkwinner(board, mark):
    # if there is 4 in a row or col, or diagonally
    return horizontalcheck(board, mark) or verticalcheck(board, mark) or diagonalcheck(board, mark) or isTie(board)


def horizontalcheck(board, mark):
    for col in range(COLUMNS - 3):
        for row in range(ROWS):
            if board[row][col] == mark and board[row][col + 1] == mark and board[row][col + 2] == mark and \
                    board[row][col + 3] == mark:
                return True


def verticalcheck(board, mark):
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == mark and board[row + 1][col] == mark and board[row + 2][col] == mark and \
                    board[row + 3][col] == mark:
                return True


def diagonalcheck(board, mark):
    # Check the positive sloped diagonal
    for col in range(COLUMNS - 3):
        for row in range(ROWS - 3):
            if board[row][col] == mark and board[row + 1][col + 1] == mark and board[row + 2][col + 2] == mark and \
                    board[row + 3][col + 3] == mark:
                return True

    # check the negatively sloped diagonal
    for col in range(COLUMNS - 3):
        for row in range(3, ROWS):  # Starting at 3
            if board[row][col] == mark and board[row - 1][col + 1] == mark and board[row - 2][col + 2] == mark and \
                    board[row - 3][col + 3] == mark:  # We are going down the rows
                return True


def printboard(board):
    print(np.flip(board, 0))  # flips the board so then the most recent will be in the lowest place

def drawboard(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SCALE, r * SCALE + SCALE, SCALE, SCALE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SCALE + SCALE / 2), int(r * SCALE + SCALE + SCALE / 2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SCALE + SCALE / 2), height - int(r * SCALE + SCALE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SCALE + SCALE / 2), height - int(r * SCALE + SCALE / 2)), RADIUS)
    pygame.display.update()

