import tkinter as tk
from tkinter import messagebox

class MyGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pierwszy program w python GUI tkinter")
        self.root.geometry('600x400+50+20')
        self.root.attributes('-alpha', 0.8)
        self.root.config(background = "Light Blue")
        self.root.attributes('-topmost', 1)

        self.menubar = tk.Menu(self.root)

        self.filemenu1 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu1.add_command(label='Close', command=self.zamknij)
        self.filemenu1.add_command(label='Clear', command=self.wyczysc)

        self.filemenu2 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu2.add_command(label='wiadomosc', command=self.show_message)
        self.filemenu2.add_command(label='wyjscie', command=exit)

        self.menubar.add_cascade(menu=self.filemenu1, label='settings')
        self.menubar.add_cascade(menu=self.filemenu2, label='others')
        self.root.config(menu=self.menubar)

        self.label = tk.Label(self.root, text='moj tekst')
        self.label.config(
            background='#555',
            fg='#F00',
            font=('Arial', 20),
            padx=20,
            pady=20
        )
        self.label.pack()



        self.root.mainloop()

    def zamknij(self):
        print('zamknij')
        if messagebox.askyesno(title='Potwierdzenie', message='Czy na pewno chcesz zamknąc?'):
            self.root.destroy()

    def wyczysc(self):
        pass

    def show_message(self):
        pass


MyGui()