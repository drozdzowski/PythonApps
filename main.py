"""
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 589a610cacb70fac3db1ddcf1e00fa529d4ff1c5
GUI Random Number Generator - Tkinter
"""
import tkinter as tk
from tkinter import messagebox
import random

class RandomNumberGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Number Generator")
        self.min_label = tk.Label(root, text="Min Value:")
        self.min_label.grid(row=0, column=0)
        self.min_entry = tk.Entry(root)
        self.min_entry.insert(0, "1")
        self.min_entry.grid(row=0, column=1)
        self.max_label = tk.Label(root, text="Max Value:")
        self.max_label.grid(row=1, column=0)
        self.max_entry = tk.Entry(root)
        self.max_entry.insert(0, "1000")
        self.max_entry.grid(row=1, column=1)
        self.generate_button = tk.Button(root, text="Generate", command=self.generate_number)
        self.generate_button.grid(row=2, column=0, columnspan=2)
        self.result_label = tk.Label(root, text="Result: ")
        self.result_label.grid(row=3, column=0, columnspan=2)

    def generate_number(self):
        try:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
            if min_val > max_val:
                messagebox.showerror("Error", "Min value must be less than or equal to Max value.")
                return
            result = random.randint(min_val, max_val)
            self.result_label.config(text=f"Result: {result}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomNumberGeneratorGUI(root)
<<<<<<< HEAD
=======
=======
Tic Tac Toe Game - GUI Version (Tkinter)
"""
import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text='', font=('Arial', 32), width=4, height=2,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def on_click(self, row, col):
        if self.board[row][col] == '':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_win(self.current_player):
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
                self.buttons[i][j].config(text='')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
>>>>>>> 167f88b49261b24dcdfd7a24860cc622c57bbcd5
>>>>>>> 589a610cacb70fac3db1ddcf1e00fa529d4ff1c5
    root.mainloop()
