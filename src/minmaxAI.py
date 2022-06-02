import math  # for the random number generator
import random
import sys

import numpy as np  # for the matrix
import pygame  # for the graphics

ROWS = 6
COLUMNS = 7

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Turn values
PLAYER = 0
COMPUTER_PLAYER = 1

# Mark values
PLAYER_MARK = 1
COMPUTER_PLAYER_MARK = 2
AVAILABLE = 0

WINDOW_LENGTH = 4


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


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_MARK
    if piece == PLAYER_MARK:
        opp_piece = COMPUTER_PLAYER_MARK

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(AVAILABLE) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(AVAILABLE) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(AVAILABLE) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def getValidLocation(board):
    validlocations = []
    for c in range(COLUMNS):
        if isavailable(board, c):
            validlocations.append(col)
    return validlocations


def bestmove(board, piece):
    bestScore = 0
    validlocations = getValidLocation(board)
    bestcol = random.choice(validlocations)
    for c in validlocations:
        row = getnextavailablerow(board, c)
        tempboard = board.copy()  # any modifications will not change the original
        makemove(tempboard, row, col, piece)

        sum = score_position(tempboard, piece)

        if sum > bestScore:
            bestScore = sum
            bestcol = col
    return bestcol


def drawboard(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SCALE, r * SCALE + SCALE, SCALE, SCALE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SCALE + SCALE / 2), int(r * SCALE + SCALE + SCALE / 2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == PLAYER_MARK:
                pygame.draw.circle(screen, RED, (
                    int(c * SCALE + SCALE / 2), height - int(r * SCALE + SCALE / 2)), RADIUS)
            elif board[r][c] == COMPUTER_PLAYER_MARK:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SCALE + SCALE / 2), height - int(r * SCALE + SCALE / 2)), RADIUS)
    pygame.display.update()


board = makeboard()
print(board)

endgame = False
turn = random.randint(PLAYER, COMPUTER_PLAYER)  # random starting

# initializing pygame
pygame.init()

SCALE = 100  # unit is in pixels

width = COLUMNS * SCALE
height = (ROWS + 1) * SCALE
size = (width, height)

RADIUS = int(SCALE / 2 - 5)

screen = pygame.display.set_mode(size)
drawboard(board)
pygame.display.update()

pygame.display.update()

font = pygame.font.SysFont("calibri", 75)
while not endgame:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SCALE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SCALE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SCALE))
            # P1 input
            if turn == 0:
                posx = event.pos[0]  # between 0 and 700 pixels
                col = int(math.floor(posx / SCALE))

                if isavailable(board, col):
                    row = getnextavailablerow(board, col)
                    makemove(board, row, col, PLAYER_MARK)

                    if checkwinner(board, PLAYER_MARK):
                        label = font.render("Player 1 won !", 1, RED)
                        screen.blit(label, (40, 10))
                        endgame = True

                    if turn == PLAYER:
                        turn = COMPUTER_PLAYER
                    else:
                        turn = PLAYER

                    printboard(board)
                    drawboard(board)

    # P2 input
    if turn == COMPUTER_PLAYER and not endgame:

        # col = random.randint(0, COLUMNS -1)

        col = bestmove(board, COMPUTER_PLAYER_MARK)
        if isavailable(board, col):
            pygame.time.wait(500)

            row = getnextavailablerow(board, col)
            makemove(board, row, col, COMPUTER_PLAYER_MARK)

            if checkwinner(board, COMPUTER_PLAYER_MARK):
                label = font.render("Player 2 won !", 1, YELLOW)
                screen.blit(label, (40, 10))
                endgame = True

            printboard(board)
            drawboard(board)
            # Switching the player turns
            if turn == PLAYER:
                turn = COMPUTER_PLAYER
            else:
                turn = PLAYER

            if endgame:
                pygame.time.wait(3000)  # waits for 3 seconds before closing the window
