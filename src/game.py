import sys
from TwoPlayers import *
from easyAI import *
# from medAI import *
# from expertAI import *
print()
print("======= WELCOME TO CONNECT 4 ========")

game_type = int(input("chose (1) to play with two players or (2) to play with AI or (0) to exit the game: "))

if game_type == 1:
    startgameTwoPlayers()
elif game_type == 2:
    level_choice = int(input("chose (1) to play against an easy AI or (2) for an expert AI: "))
    if level_choice == 1:
        easyAIstartgame()
#     elif level_choice == "M":
#         pass
#     else:
#         pass
elif game_type == 0:
    sys.exit()
