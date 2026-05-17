import math
import random
import tkinter as tk
from tkinter import messagebox

HUMAN = "X"
AI = "O"
EMPTY = " "

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Хрестики-Нулики з ШІ")
        self.root.resizable(False, False)
        
        # Налаштування складності (0.4 = 40% випадкових ходів)
        self.difficulty = 0.4
        
        self.board = [EMPTY] * 9
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        # Створюємо сітку кнопок 3х3
        for i in range(9):
            btn = tk.Button(
                self.root, 
                text=EMPTY, 
                font=("Arial", 24, "bold"), 
                width=5, 
                height=2,
                bg="#f0f0f0",
                command=lambda idx=i: self.human_move(idx)
            )
            # Розміщення у сітці (row, column)
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)

    def check_winner(self):
        wins = [
            (0,1,2), (3,4,5), (6,7,8), # Горизонталі
            (0,3,6), (1,4,7), (2,5,8), # Вертикалі
            (0,4,8), (2,4,6)           # Діагоналі
        ]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] != EMPTY:
                return self.board[a]
        if EMPTY not in self.board:
            return "DRAW"
        return None

    def minimax(self, is_ai):
        result = self.check_winner()
        if result == AI: return 1
        elif result == HUMAN: return -1
        elif result == "DRAW": return 0

        if is_ai:
            best_score = -math.inf
            for i in range(9):
                if self.board[i] == EMPTY:
                    self.board[i] = AI
                    score = self.minimax(False)
                    self.board[i] = EMPTY
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if self.board[i] == EMPTY:
                    self.board[i] = HUMAN
                    score = self.minimax(True)
                    self.board[i] = EMPTY
                    best_score = min(best_score, score)
            return best_score

    def ai_move(self):
        # Логіка складності (випадковий хід)
        if random.random() < self.difficulty:
            available_moves = [i for i, spot in enumerate(self.board) if spot == EMPTY]
            if available_moves:
                move = random.choice(available_moves)
                self.make_move(move, AI)
                return

        # Логіка Minimax
        best_score = -math.inf
        best_move = None
        for i in range(9):
            if self.board[i] == EMPTY:
                self.board[i] = AI
                score = self.minimax(False)
                self.board[i] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = i
                    
        if best_move is not None:
            self.make_move(best_move, AI)

    def human_move(self, index):
        # Якщо клітинка зайнята, нічого не робимо
        if self.board[index] != EMPTY:
            return
        
        # Хід людини
        self.make_move(index, HUMAN)
        
        # Перевірка після ходу людини
        if self.check_game_over():
            return
        
        # Хід комп'ютера (з невеликою затримкою для реалістичності)
        self.root.after(300, self.ai_move)

    def make_move(self, index, player):
        self.board[index] = player
        # Візуальне оновлення кнопки
        color = "#2196F3" if player == HUMAN else "#F44336"
        self.buttons[index].config(text=player, state="disabled", disabledforeground=color)
        
        # Перевірка після ходу ШІ
        self.check_game_over()

    def check_game_over(self):
        result = self.check_winner()
        if result:
            if result == HUMAN:
                messagebox.showinfo("Результат", "Ти виграв! 🎉")
            elif result == AI:
                messagebox.showinfo("Результат", "Комп'ютер виграв! 🤖")
            else:
                messagebox.showinfo("Результат", "Нічия! 🤝")
            
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.board = [EMPTY] * 9
        for btn in self.buttons:
            btn.config(text=EMPTY, state="normal", bg="#f0f0f0")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()