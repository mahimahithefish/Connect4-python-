import random
import math
import sys
from board import *

def easyAIstartgame():
    board = makeboard()
    printboard(board)
    game_over = False
    turn = random.randint(PLAYER, COMPUTER_PLAYER) # taking random turns


    pygame.init()

    drawboard(board)
    pygame.display.update()

    font = pygame.font.SysFont("calibri", 75)  # FOnt for displaying the winner text

    while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SCALE))
                    posx = event.pos[0]
                    if turn == PLAYER:
                        pygame.draw.circle(screen, RED, (posx, int(SCALE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, YELLOW, (posx, int(SCALE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SCALE))

                    if turn == PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx / SCALE))

                        if isavailable(board, col):
                            row = getnextavailablerow(board, col)
                            makemove(board, row, col, PLAYER_MARK)

                            if checkwinner(board, PLAYER_MARK):
                                label = font.render("PLAYER 1 WON!", 1, RED)
                                screen.blit(label, (40, 10))
                                game_over = True
                            elif isTie(board):  # Check if the board is full
                                label = font.render("Game is a Draw", 1, WHITE)
                                screen.blit(label, (40, 10))
                                endgame = True

                        printboard(board)
                        drawboard(board)

                        turn = COMPUTER_PLAYER # Switching players

                # Computer's turn will make move
                if turn == COMPUTER_PLAYER and not game_over:

                    col = random.randint(0, COLUMNS - 1)

                    if isavailable(board, col):
                        pygame.time.wait(500)
                        row = getnextavailablerow(board, col)
                        makemove(board, row, col, COMPUTER_PLAYER_MARK)

                        if checkwinner(board, COMPUTER_PLAYER_MARK):
                            label = font.render("PLAYER 2 WON!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True
                        elif isTie(board):  # Check if the board is full
                            label = font.render("Game is a Draw", 1, WHITE)
                            screen.blit(label, (40, 10))
                            endgame = True

                    printboard(board)
                    drawboard(board)

                    turn = 0 # Switching players

                    if game_over:
                        pygame.time.wait(5000)