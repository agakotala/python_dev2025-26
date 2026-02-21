import tkinter as tk
from tkinter import messagebox

class MyGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('600x400+50+20')

        self.label1 = tk.Label(self.root, text='moj textxxxxxxxxxx')
        self.label1.config(
            background="#555",
            fg="#ccc",
            font=("Arial", 20),
            padx=20,
            pady=10
        )

        self.label2 = tk.Label(self.root, text='moj text2')
        self.label2.config(
            background="#AAA",
            fg="#00F",
            font=("Arial", 20),
            padx=20,
            pady=10)

        self.label1.grid(row=0, column=0, rowspan=1, columnspan=2)
        self.label2.grid(row=1, column=2)

        self.root.mainloop()

MyGui()