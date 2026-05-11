import random
import math

N = 5

def random_board(N):
    return [random.randint(0, N-1) for _ in range(N)]

def conflicts(board):
    count = 0
    for i in range(N):
        for j in range(i+1, N):
            if board[i] == board[j] or abs(board[i]-board[j]) == abs(i-j):
                count += 1
    return count

def print_board(board):
    for i in range(N):
        row = ""
        for j in range(N):
            row += "Q " if board[i] == j else ". "
        print(row)
    print("\nConflicts:", conflicts(board))

def simulated_annealing():
    board = random_board(N)
    
    print("Початкова кількість конфліктів:", conflicts(board))
    
    T = 100
    alpha = 0.93
    while T > 0.1 and conflicts(board) != 0:
        i = random.randint(0, N-1)
        old_value = board[i]
        board[i] = random.randint(0, N-1)
        delta = conflicts(board) - conflicts(board[:i] + [old_value] + board[i+1:])
        if delta > 0 and math.exp(-delta/T) < random.random():
            board[i] = old_value
        T *= alpha
    return board

solution = simulated_annealing()
print_board(solution)