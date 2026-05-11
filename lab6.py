import math
import random  

HUMAN = "X"
AI = "O"
EMPTY = " "

def create_board():
    return [EMPTY] * 9

def print_board(board):
    for i in range(3):
        print(board[i*3:(i+1)*3])
    print()

def check_winner(board):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    if EMPTY not in board:
        return "DRAW"
    return None

def minimax(board, is_ai):
    result = check_winner(board)
    if result == AI: return 1
    elif result == HUMAN: return -1
    elif result == "DRAW": return 0

    if is_ai:
        best_score = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                score = minimax(board, False)
                board[i] = EMPTY
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                score = minimax(board, True)
                board[i] = EMPTY
                best_score = min(best_score, score)
        return best_score

def ai_move(board, difficulty=0.3):
    if random.random() < difficulty:
        available_moves = [i for i, spot in enumerate(board) if spot == EMPTY]
        move = random.choice(available_moves)
        board[move] = AI
        return

    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, False)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                best_move = i
    board[best_move] = AI

def human_move(board):
    while True:
        try:
            move = int(input("Введи позицію (0-8): "))
            if 0 <= move <= 8 and board[move] == EMPTY:
                board[move] = HUMAN
                break
            else:
                print("Клітинка зайнята або невірна позиція!")
        except ValueError:
            print("Введи число!")

def play():
    board = create_board()
    diff = 0.4 
    
    print(f"Гра починається! Рівень помилок комп'ютера: {diff*100}%")
    print_board(board)

    while True:
        human_move(board)
        print_board(board)
        if check_winner(board): break

        print("Хід комп'ютера...")
        ai_move(board, difficulty=diff)
        print_board(board)
        if check_winner(board): break

    result = check_winner(board)
    if result == HUMAN: print("Ти виграв! 🎉")
    elif result == AI: print("Комп'ютер виграв!")
    else: print("Нічия!")

if __name__ == "__main__":
    play()