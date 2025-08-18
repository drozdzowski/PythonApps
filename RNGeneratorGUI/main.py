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
        self.root.configure(bg="#f0f0f0")

        self.title_label = tk.Label(root, text="Random Number Generator", font=("Arial", 20, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=10)

        self.input_frame = tk.Frame(root, bg="#f0f0f0")
        self.input_frame.pack(pady=10)

        self.min_label = tk.Label(self.input_frame, text="Min Value:", font=("Arial", 12), bg="#f0f0f0")
        self.min_label.grid(row=0, column=0, padx=5, pady=5)
        self.min_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=8)
        self.min_entry.insert(0, "1")
        self.min_entry.grid(row=0, column=1, padx=5, pady=5)

        self.max_label = tk.Label(self.input_frame, text="Max Value:", font=("Arial", 12), bg="#f0f0f0")
        self.max_label.grid(row=1, column=0, padx=5, pady=5)
        self.max_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=8)
        self.max_entry.insert(0, "1000")
        self.max_entry.grid(row=1, column=1, padx=5, pady=5)

        self.generate_button = tk.Button(root, text="Generate", font=("Arial", 12), command=self.generate_number, bg="#e0e0e0")
        self.generate_button.pack(pady=10)

        self.result_label = tk.Label(root, text="Result: ", font=("Arial", 16), bg="#f0f0f0")
        self.result_label.pack(pady=10)

        self.copy_button = tk.Button(root, text="Copy Result", font=("Arial", 10), command=self.copy_result, bg="#e0e0e0")
        self.copy_button.pack(pady=5)

    def generate_number(self):
        try:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
            if min_val > max_val:
                messagebox.showerror("Error", "Min value must be less than or equal to Max value.")
                return
            result = random.randint(min_val, max_val)
            self.result_label.config(text=f"Result: {result}")
            self.last_result = str(result)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")
            self.last_result = ""

    def copy_result(self):
        if hasattr(self, 'last_result') and self.last_result:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.last_result)
            messagebox.showinfo("Copied", "Result copied to clipboard!")
        else:
            messagebox.showwarning("No Result", "No result to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomNumberGeneratorGUI(root)
    root.mainloop()
