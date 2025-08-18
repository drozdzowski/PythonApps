"""
Tic Tac Toe Game - GUI Version (Tkinter)
"""

import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#f0f0f0")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.x_score = 0
        self.o_score = 0

        self.title_label = tk.Label(root, text="Tic Tac Toe", font=("Arial", 24, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=10)

        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack(pady=5)

        self.board_frame = tk.Frame(root, bg="#f0f0f0")
        self.board_frame.pack(padx=20, pady=10)
        self.create_board()

        self.restart_button = tk.Button(root, text="Restart", font=("Arial", 12), command=self.reset_board, bg="#e0e0e0")
        self.restart_button.pack(pady=10)

    def get_score_text(self):
        return f"Score - X: {self.x_score} | O: {self.o_score}"

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.board_frame, text='', font=('Arial', 32), width=4, height=2,
                                command=lambda row=i, col=j: self.on_click(row, col), bg="#ffffff", relief="ridge")
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
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

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
                self.buttons[i][j].config(text='', state="normal", bg="#ffffff")
        self.current_player = 'X'

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
