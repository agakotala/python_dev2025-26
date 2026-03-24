import tkinter as tk
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('Tkinter')

entry_test = tk.StringVar()

def button_clicked():
    msg =f'potwierdzone, wpisales: {entry_test.get()}'
    showinfo(title='Info', message=msg)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill='x', expand=True)

label = tk.Label(frame, text='Wpisz PESEL')
label.pack(fill='x', expand=True)
entry = tk.Entry(frame, textvariable=entry_test)
entry.pack(fill='x', expand=True)

button = tk.Button(frame, text='kliknij', command=button_clicked)
button.pack(fill='x', pady=20, expand=True)

root.mainloop()