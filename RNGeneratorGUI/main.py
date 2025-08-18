"""
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
    root.mainloop()
