from board import *

WINDOW_LENGTH = 4


def evaluate_window(window, mark):
    score = 0
    opponent = PLAYER_MARK

    if mark == PLAYER_MARK:
        opponent = COMPUTER_PLAYER_MARK

    if window.count(mark) == 4:
        score += 100

    elif window.count(mark) == 3 and window.count(AVAILABLE) == 1:
        score += 5

    elif window.count(mark) == 2 and window.count(AVAILABLE) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(AVAILABLE) == 1:
        score -= 4

    return score


def score_position(board, mark):
    score = 0

    score += scoreCenter(board, mark)  # Scoring the center column
    score += scoreHorizonally(board, mark)  # scoring the row
    score += scoreVertically(board, mark)  # Scoring the column
    score += scoreDiag(board, mark)  # Scoring the Diagonal
    return score


def scoreCenter(board, mark):  # scoring the center column
    score = 0
    centerArray = [int(i) for i in list(board[:, COLUMNS // 2])]
    center_count = centerArray.count(mark)
    score += center_count * 3

    return score


def scoreHorizonally(board, mark):
    score = 0
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, mark)

    return score


def scoreVertically(board, mark):
    score = 0
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, mark)
    return score


def scoreDiag(board, mark):
    score = 0

    for r in range(ROWS - 3):  # positive slope
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, mark)

    for r in range(ROWS - 3):  # negative slope
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, mark)

    return score


def is_terminal_node(board):
    return checkwinner(board, PLAYER_MARK) or checkwinner(board, COMPUTER_PLAYER_MARK) or isTie(board)


def minimax(board, depth, alpha, beta, maxPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if checkwinner(board, COMPUTER_PLAYER_MARK):
                return (None, 100000000000000)
            elif checkwinner(board, PLAYER_MARK):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, COMPUTER_PLAYER_MARK))
    if maxPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getnextavailablerow(board, col)
            b_copy = board.copy()
            makemove(b_copy, row, col, COMPUTER_PLAYER_MARK)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getnextavailablerow(board, col)
            b_copy = board.copy()
            makemove(b_copy, row, col, PLAYER_MARK)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMNS):
        if isavailable(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = getnextavailablerow(board, col)
        temp_board = board.copy()
        makemove(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == PLAYER_MARK:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == COMPUTER_PLAYER_MARK:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = makeboard()
printboard(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("calibri", 75)

turn = random.randint(PLAYER, COMPUTER_PLAYER)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if isavailable(board, col):
                    row = getnextavailablerow(board, col)
                    makemove(board, row, col, PLAYER_MARK)

                    if checkwinner(board, PLAYER_MARK):
                        label = myfont.render("PLAYER 1 WINS ! ", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    printboard(board)
                    draw_board(board)

    # # Ask for Player 2 Input
    if turn == COMPUTER_PLAYER and not game_over:

        # col = random.randint(0, COLUMNS-1)
        # col = pick_best_move(board, COMPUTER_PLAYER_MARK)
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if isavailable(board, col):
            # pygame.time.wait(500)
            row = getnextavailablerow(board, col)
            makemove(board, row, col, COMPUTER_PLAYER_MARK)

            if checkwinner(board, COMPUTER_PLAYER_MARK):
                label = myfont.render("PLAYER 2 WINS !", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            printboard(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
