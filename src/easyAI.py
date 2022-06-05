import random
import math
import sys
from board import *



def easyAIstartgame():
    board = makeboard()
    printboard(board)
    game_over = False
    turn = 0

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
                    if turn == 0:
                        pygame.draw.circle(screen, RED, (posx, int(SCALE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, YELLOW, (posx, int(SCALE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SCALE))

                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx / SCALE))

                        if isavailable(board, col):
                            row = getnextavailablerow(board, col)
                            makemove(board, row, col, 1)

                            if checkwinner(board, 1):
                                label = font.render("PLAYER 1 WON!", 1, RED)
                                screen.blit(label, (40, 10))
                                game_over = True
                            elif isTie(board):  # Check if the board is full
                                label = font.render("Game is a Draw", 1, WHITE)
                                screen.blit(label, (40, 10))
                                endgame = True

                        printboard(board)
                        drawboard(board)

                        turn = 1 # Switching players

                # Computer's turn will make move
                if turn == 1 and not game_over:

                    col = random.randint(0, COLUMNS - 1)

                    if isavailable(board, col):
                        pygame.time.wait(500)
                        row = getnextavailablerow(board, col)
                        makemove(board, row, col, 2)

                        if checkwinner(board, 2):
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
                        pygame.time.wait(3500)