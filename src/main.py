import numpy as np  # this library allows us to use a matrix

ROWS = 6
COLUMNS = 7

def makeboard():
    # Top most row is the 5th row
    board = np.zeros((ROWS, COLUMNS))  # make a matrix of 6 rows and 7 columns
    return board


def makemove(board, row, col, mark):
    board[row][col] = mark


def isavailable(board, col): # Checks if the given column is available to make a move
    return board[ROWS - 1][col] == 0  # If it is true then we are good to make a move in this column!


def getnextavailablerow(board, col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row

def checkwinner(board, mark):
    # check horizontally

    # check vertically
    # Check diagonally

def horizontalcheck(board, mark):
    pass
def verticalcheck(board, mark):
    pass
def diagonalcheck(board, mark):
    pass

def printboard(board):
    print(np.flip(board, 0))  # flips the board so then the most recent will be in the lowest place

board = makeboard()
print(board)
endgame = False

turn = 0
while not endgame:
    # P1 input
    if turn == 0:
        col = int(input("Player 1 Pick a column (0 - 6): "))
        if isavailable(board, col):
            row = getnextavailablerow(board, col)
            makemove(board, row, col, 1)

    # P2 input
    else:
        col = int(input("Player 2 Pick a column (0 - 6): "))
        if isavailable(board, col):
            row = getnextavailablerow(board, col)
            makemove(board, row, col, 2)
    printboard(board)
    if turn == 0:
        turn = 1
    else:
        turn = 0

