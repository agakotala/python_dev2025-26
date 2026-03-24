from tkinter import *

def pojedyncze(e):
    print(e)
    print('Nacisnieto pojedynczo')

def podwojne(e):
    print(e)
    print('podwojne klikniecie')

button = Button(None, text='Kliknij mysza')
button.pack()

button.bind('<Button-1>', pojedyncze)
button.bind('<Double-1>', podwojne)
button.bind('<Button-2>', pojedyncze)
button.bind('<Double-2>', podwojne)
button.bind('<Button-3>', pojedyncze)
button.bind('<Double-3>', podwojne)

button.mainloop()