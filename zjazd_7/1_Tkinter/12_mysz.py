import tkinter as tk

def pozycja(e):
    print(e)
    print(f'{e.x} , {e.y}')


root = tk.Tk()
root.title('Tkinter')
root.attributes('-alpha', 0.6)
root.attributes('-topmost', 1)

root.bind('<Motion>', pozycja)

root.mainloop()