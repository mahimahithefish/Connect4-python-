print()
print("============= WELCOME TO CONNECT 4 GAME =============")
print()

thanks = "Thank you for playing!"

game_choice = input("AI or 2 PLAYERS game? enter Q to QUIT game ")
game_choice.lower()
if game_choice == "ai":
    game_level = input("EASY or EXPERT AI? ")
    print()
    if game_level == "easy":
        from easyAI import *
        startEasyAI()
        print(thanks)
    else:
        pass
elif game_choice == "2 players":
    from TwoPlayers import *
    startTwoGame()
    print(thanks)
else:
    print("Quitting game.........")