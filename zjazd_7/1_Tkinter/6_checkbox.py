import tkinter as tk
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('Tkinter')

agreement = tk.StringVar()

def agreement_changed():
    showinfo(title='zaznacz', message=agreement.get())
tk.Checkbutton(root,
               text='zaznacz', command=agreement_changed,
               variable=agreement,
               onvalue='zaznaczono', offvalue='odznaczono').pack()

root.mainloop()