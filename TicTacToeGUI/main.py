"""
Tic Tac Toe Game - GUI Version (Tkinter)
"""

import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        import random
        self.root = root
        self.root.title("Tic Tac Toe")
        self.pastel_bg = self.random_pastel()
        self.root.configure(bg=self.pastel_bg)
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.x_score = 0
        self.o_score = 0

        self.title_label = tk.Label(root, text="Tic Tac Toe", font=("Arial", 24, "bold"), bg=self.pastel_bg)
        self.title_label.pack(pady=10)

        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 14), bg=self.pastel_bg)
        self.score_label.pack(pady=5)

        self.board_frame = tk.Frame(root, bg=self.pastel_bg)
        self.board_frame.pack(padx=20, pady=10)
        self.create_board()

        self.restart_button = tk.Button(root, text="Restart", font=("Arial", 12), command=self.reset_board, bg=self.random_pastel())
        self.restart_button.pack(pady=10)

    def random_pastel(self):
        import random
        r = random.randint(180, 255)
        g = random.randint(180, 255)
        b = random.randint(180, 255)
        return f'#{r:02x}{g:02x}{b:02x}'

    def get_score_text(self):
        return f"Score - X: {self.x_score} | O: {self.o_score}"

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.board_frame, text='', font=('Arial', 32), width=4, height=2,
                                command=lambda row=i, col=j: self.on_click(row, col), bg=self.random_pastel(), relief="ridge")
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

    def on_click(self, row, col):
        if self.board[row][col] == '':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, disabledforeground="#333333")
            self.buttons[row][col].config(state="disabled")
            if self.check_win(self.current_player):
                if self.current_player == 'X':
                    self.x_score += 1
                else:
                    self.o_score += 1
                self.score_label.config(text=self.get_score_text())
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
                return
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
                return
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if self.current_player == 'O':
                self.root.after(500, self.ai_move)

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            row, col = best_move
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O', disabledforeground="#333333")
            self.buttons[row][col].config(state="disabled")
            if self.check_win('O'):
                self.o_score += 1
                self.score_label.config(text=self.get_score_text())
                messagebox.showinfo("Game Over", "Player O (AI) wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'X'

    def minimax(self, board, depth, is_maximizing):
        if self.check_win_on_board(board, 'O'):
            return 1
        elif self.check_win_on_board(board, 'X'):
            return -1
        elif all([board[i][j] != '' for i in range(3) for j in range(3)]):
            return 0
        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def check_win_on_board(self, board, player):
        for i in range(3):
            if all([board[i][j] == player for j in range(3)]):
                return True
            if all([board[j][i] == player for j in range(3)]):
                return True
        if all([board[i][i] == player for i in range(3)]):
            return True
        if all([board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def check_win(self, player):
        for i in range(3):
            if all([self.board[i][j] == player for j in range(3)]):
                return True
            if all([self.board[j][i] == player for j in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]):
            return True
        if all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def check_draw(self):
        return all([self.board[i][j] != '' for i in range(3) for j in range(3)])

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state="normal", bg=self.random_pastel())
        self.current_player = 'X'

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
