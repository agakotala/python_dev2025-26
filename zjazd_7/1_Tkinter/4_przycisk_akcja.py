import tkinter as tk
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('Tkinter')

def download_clicked():
    showinfo(title='Information', message='Button clicked')

icon = tk.PhotoImage(file='./merito.png')
download_button = tk.Button(root, image=icon, command=download_clicked)
download_button.pack(ipadx=5, ipady=5)

root.mainloop()