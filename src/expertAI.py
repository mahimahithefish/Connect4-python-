import math  # for the random number generator
import random
import sys

from board import *

# Turn values
PLAYER = 0
COMPUTER_PLAYER = 1

# Mark values
PLAYER_MARK = 1
COMPUTER_PLAYER_MARK = 2
AVAILABLE = 0

WINDOW_LENGTH = 4



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




def isTerminalnode(board):
    return checkwinner(board, PLAYER_MARK) or checkwinner(board, AVAILABLE) or len(getValidLocation(board)) == 0

def minimax(board, depth, maxplayer ):
    validlocations = getValidLocation(board)
    is_terminal = isTerminalnode(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if checkwinner(board, COMPUTER_PLAYER_MARK):
                return {None, 10000}
            elif checkwinner(board, PLAYER_MARK):
                return {None, -10000}
            else: #board that is not terminal
                return {None, 0}
        else:
            return {None, score_position(board, COMPUTER_PLAYER_MARK )}
    if maxplayer:
        value = -math.inf
        columns = random.choice(validlocations)
        for col in validlocations:
            row = getnextavailablerow(board, col)
            bcopy  = board.copy()
            makemove(bcopy, row, col, COMPUTER_PLAYER_MARK)
            new_score = minimax(bcopy, depth -1, False)[1]
            if new_score > value:
                value = new_score
                columns = col
            return columns, value
    else:
        value = math.inf
        columns = random.choice(validlocations)

        for col in validlocations:
            row = getnextavailablerow(board, col)
            bcopy = board.copy()
            makemove(bcopy, row, col, PLAYER_MARK)
            new_score =  minimax(bcopy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                columns = col
            return columns, value

board = makeboard()
print(board)

endgame = False
turn = random.randint(PLAYER, COMPUTER_PLAYER)  # random starting

# initializing pygame
pygame.init()


drawboard(board)
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
        col, minimax_score = minimax(board, 4, True)
        # col = bestmove(board, COMPUTER_PLAYER_MARK)
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
