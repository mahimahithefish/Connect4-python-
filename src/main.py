import sys

import numpy as np  # this library allows us to use a matrix
import pygame

ROWS = 6
COLUMNS = 7
BLUE = (0,0,255)
BLACK = (0,0,0)

def makeboard():
    # Top most row is the 5th row
    board = np.zeros((ROWS, COLUMNS))  # make a matrix of 6 rows and 7 columns
    return board


def makemove(board, row, col, mark):
    board[row][col] = mark


def isavailable(board, col):  # Checks if the given column is available to make a move
    return board[ROWS - 1][col] == 0  # If it is true then we are good to make a move in this column!


def getnextavailablerow(board, col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row


def checkwinner(board, mark):
    # if there is 4 in a row or col, or diagonally
    return horizontalcheck(board, mark) or verticalcheck(board, mark) or diagonalcheck(board, mark)


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
    for col in range(COLUMNS):
        for row in range(ROWS):
            pygame.draw.rect(screen,BLUE, (col * SCALE, row * SCALE + SCALE, SCALE, SCALE))
            pygame.draw.circle(screen, BLACK, (int(col*SCALE + SCALE / 2), int(row*SCALE + SCALE + SCALE / 2)), RADIUS)

board = makeboard()
print(board)
endgame = False
turn = 0

# initializing pygame
pygame.init()

SCALE = 100# unit is in pixels
width = COLUMNS * SCALE
height = ROWS + 1 * SCALE
RADIUS = int(SCALE / 2 - 5)

windowsize = (width, height)
screen = pygame.display.set_mode(windowsize)
drawboard(board)

pygame.display.update()

while not endgame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            continue
            # P1 input
            # if turn == 0:
            #     col = int(input("Player 1 Pick a column (0 - 6): "))
            #     if isavailable(board, col):
            #         row = getnextavailablerow(board, col)
            #         makemove(board, row, col, 1)
            #     if checkwinner(board, 1):
            #         print("Player 1 won!")
            #         endgame = True
            #
            # # P2 input
            # else:
            #     col = int(input("Player 2 Pick a column (0 - 6): "))
            #     if isavailable(board, col):
            #         row = getnextavailablerow(board, col)
            #         makemove(board, row, col, 2)
            #     if checkwinner(board, 2):
            #         print("Player 2 won!")
            #         endgame = True

            # printboard(board)
            #
            # # Switching the player turns
            # if turn == 0:
            #     turn = 1
            # else:
            #     turn = 0

