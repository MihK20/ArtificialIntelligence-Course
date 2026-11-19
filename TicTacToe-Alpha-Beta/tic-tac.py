import math

def has_won(board, player):
    for row in board:
        if all(elem == player for elem in row):
            return True

        
    for i in range(3):
        column = []
        for j in range(3):
            column.append(board[j][i])
        if all(elem == player for elem in column):
            return True

        
    d1 = [board[i][i] for i in range(3)]
    d2 = [board[i][2-i] for i in range(3)]
    if all(elem == player for elem in d1):
        return True
    if all(elem == player for elem in d2):
        return True

    return False

def full_board(board):
    return all(space != '_' for row in board for space in row)

def is_terminal(board):
    return has_won(board, 'O') or has_won(board, 'X') or full_board(board)

def opponent(player):
    return 'X'if player == 'O' else 'O'

def succ_fn(board, player):
    positions = []
    for x in range(3):
        for y in range(3):
            if board[x][y]=='_':
                new_board = [row[:] for row in board]
                new_board[x][y] = player
                positions.append((new_board,(x,y)))

    return positions

def negamax(board, player, alpha:float | int , beta: float | int) -> float | int:
    if is_terminal(board):
        depth = sum(1 for row in board for elem in row if elem!='_')
        return 10 - depth if has_won(board, player) else depth - 10 if has_won(board, opponent(player)) else 0

    val = -math.inf
    for next_state, action in succ_fn(board, player):
        val = max(val, -negamax(next_state, opponent(player), -beta, -alpha))
        if val >= beta:
            return val
        alpha = max(alpha, val)
    return val

def solve(board, player):
    val = -math.inf
    best_action = None
    for next_state, action in succ_fn(board, player):
        result = -negamax(next_state, opponent(player), -math.inf, math.inf)
        if result > val:
            val = result
            best_action = action
    x, y = best_action
    return x + 1, y + 1

def judge(board, turn):
    if is_terminal(board):
        print(-1)
    else:
        x, y = solve(board, turn)
        print(f"{x} {y}")

def getPos():
    xy = input().split()
    x=xy[0]
    y=xy[1]
    return (int(x)-1, int(y)-1)

def printBoard(board):    
    border = "+---+---+---+"
    j = 0
    for i in range(7):
        if i%2==0:
            print(border)
        else:
            row= "| "+ board[j][0]+ " | "+ board[j][1]+ " | "+ board[j][2]+ " |"
            print(str(row))
            j+=1

def game(board, first, human):
    while not is_terminal(board):
        if first == human:
            x, y = getPos()
            while board[x][y]!="_":
                print("Invalid move")
                x, y = getPos()
            board[x][y] = human
            first = opponent(human)
            printBoard(board)
        else:
            x, y = solve(board, first)
            board[x-1][y-1] = first
            first = opponent(first)
            printBoard(board)

    winner = 'O' if has_won(board, 'O') else 'X' if has_won(board, 'X') else None
    if winner:
        print(f"WINNER {winner}")
    else:
        print("DRAW")

mode = input()

if mode == 'JUDGE':
    turn = input().split()[1]
    board = []
    for i in range(7):
        row = []
        if i % 2 == 0:
            input()
        else:
            items = input().split()
            row = [item for item in items if item in ['X', 'O', '_']]
            board.append(row)

    judge(board, turn)
else:
    first = input().split()[1]
    human = input().split()[1]
    board = []
    for i in range(7):
        row = []
        if i % 2 == 0:
            input()
        else:
            items = input().split()
            row = [item for item in items if item in ['X', 'O', '_']]
            board.append(row)
    game(board, first, human)




# JUDGE
# TURN X

# GAME
# FIRST X
# HUMAN X
# +---+---+---+
# | X | O | _ |
# +---+---+---+
# | _ | X | X |
# +---+---+---+
# | X | O | _ |
# +---+---+---+