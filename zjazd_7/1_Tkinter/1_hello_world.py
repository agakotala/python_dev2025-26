import tkinter as tk

root = tk.Tk()
root.title('Tkinter')
root.geometry('600x400+200+100')    # wielkość okna i położenie
# root.resizable(True, False)
root.maxsize(800, 600)
root.minsize(200, 200)
root.attributes('-alpha', 0.6)
root.attributes('-topmost', 1)
root.iconbitmap('merito.ico')

message1 = tk.Label(root, text='Pierwszy napis')
message1.pack()

message2 = tk.Label(root, text='Drugi napis')
message2.pack()

root.mainloop()