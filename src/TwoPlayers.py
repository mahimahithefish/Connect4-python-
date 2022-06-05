from board import *
import math
import sys

def startgameTwoPlayers():
    board = makeboard()

    endgame = False
    turn = 0

    # initializing pygame
    pygame.init()

    drawboard(board)
    pygame.display.update()

    font = pygame.font.SysFont("calibri", 75)  # FOnt for displaying the winner text

    while not endgame:
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # Exiting the game without any wins
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SCALE))
                posx = event.pos[0]
                if turn == 0: # Red player's Mark will be put on the board
                    pygame.draw.circle(screen, RED, (posx, int(SCALE / 2)), RADIUS)
                else: # Yellow player's mark will be put on the board
                    pygame.draw.circle(screen, YELLOW, (posx, int(SCALE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SCALE))
                # P1 input
                if turn == 0:
                    posx = event.pos[0]  # between 0 and 700 pixels
                    col = int(math.floor(posx / SCALE))

                    if isavailable(board, col):
                        row = getnextavailablerow(board, col)
                        makemove(board, row, col, 1)

                        if checkwinner(board, 1):
                            label = font.render("PLAYER 1 WON !", 1, RED)
                            screen.blit(label, (40, 10))
                            endgame = True
                        elif isTie(board): # Check if the board is full
                            label = font.render("Game is a Draw", 1, WHITE)
                            screen.blit(label, (40, 10))
                            endgame = True

                # # P2 input
                else:
                    posx = event.pos[0]  # between 0 and 700 pixels
                    col = int(math.floor(posx / SCALE))
                    if isavailable(board, col):
                        row = getnextavailablerow(board, col)
                        makemove(board, row, col, 2)

                        if checkwinner(board, 2):
                            label = font.render("PLAYER 2 WON !", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            endgame = True
                        elif isTie(board): # Check if the board is full
                            label = font.render("Game is a Draw", 1, WHITE)
                            screen.blit(label, (40, 10))
                            endgame = True

                printboard(board)
                drawboard(board)
                # Switching the player turns
                if turn == 0:
                    turn = 1
                else:
                    turn = 0
                if endgame:
                    pygame.time.wait(2500)  # waits for 3 seconds for the gaming window to close
