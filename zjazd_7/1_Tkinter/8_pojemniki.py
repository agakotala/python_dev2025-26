import tkinter as tk

root = tk.Tk()
root.title('pojemniki')
root.geometry('400x200')
root.attributes('-alpha', 0.8)
root.attributes('-topmost', 1)

box1 = tk.Label(root, text='Pojemik 1',bg='green', fg='white')
box1.pack(ipadx=10, ipady=10, pady=10)
box2 = tk.Label(root, text='Pojemik 2',bg='red', fg='white')
box2.pack(ipadx=20, ipady=20)

root.mainloop()