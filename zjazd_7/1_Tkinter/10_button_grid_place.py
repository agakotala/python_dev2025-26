import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title('Nowy')
root.attributes('-alpha', 0.8)
root.attributes('-topmost', 1)
root.geometry('500x600+1350+230')
root.configure(bg='light blue')

click_counter = 0
current_color = 'light blue'

def add_number(number):
    textbox.insert(tk.END, str(number))

def clear_text():
    textbox.delete('1.0', tk.END)

def show_text():
    content = textbox.get('1.0', tk.END).strip()
    messagebox.showinfo('Zawartosc', f'Wpisany text:\n{content}')

def change_background():
    global current_color
    if current_color == 'light blue':
        current_color = 'light green'
    else:
        current_color = 'light blue'
    root.configure(bg=current_color)

def count_click():
    global click_counter
    click_counter += 1
    counter_label.config(text=f'Licznik: {click_counter}')

def copy_to_label():
    content = textbox.get('1.0',tk.END).strip()
    nextlabel.config(text=content)

def on_enter(event):
    show_text()


label = tk.Label(root, text='Hello', font=('Arial', 20))
label.pack(padx=20, pady=20)

#tk.Label(root, text='Hello', font=('Arial', 20)).pack(padx=20, pady=20)
textbox = tk.Text(root, height=3, font=('Arial', 20))
textbox.pack(padx=20, pady=50)

root.bind('<Return>', on_enter)

buttonframe = tk.Frame(root)

for i in range(3):
    buttonframe.columnconfigure(i, weight=1)

# buttonframe.columnconfigure(0, weight=1)
# buttonframe.columnconfigure(1, weight=1)
# buttonframe.columnconfigure(2, weight=1)

numbers = [
    ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
    ('4', 1, 0), ('5', 1, 1), ('6', 1, 2)
]

for (text, row, col) in numbers:
    btn = tk.Button(
        buttonframe,
        text=text,
        font=('Arial', 15),
        command=lambda t=text: add_number(t)
    )
    btn.grid(row=row, column=col, sticky=tk.W + tk.E)

# btn1 = tk.Button(buttonframe, text='1', font=('Arial', 15))
# btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
# btn2 = tk.Button(buttonframe, text='2', font=('Arial', 15))
# btn2.grid(row=0, column=1, sticky=tk.W+tk.E)
# btn3 = tk.Button(buttonframe, text='3', font=('Arial', 15))
# btn3.grid(row=0, column=2, sticky=tk.W+tk.E)
# btn4 = tk.Button(buttonframe, text='4', font=('Arial', 15))
# btn4.grid(row=1, column=0, sticky=tk.W+tk.E)
# btn5 = tk.Button(buttonframe, text='5', font=('Arial', 15))
# btn5.grid(row=1, column=1, sticky=tk.W+tk.E)
# btn6 = tk.Button(buttonframe, text='6', font=('Arial', 15))
# btn6.grid(row=1, column=2, sticky=tk.W+tk.E)

# nextbtn = tk.Button(root, text='Label')
# nextbtn.place(x=200, y=400, height=100, width=100)
#
# nextlabel = tk.Label(root, text='Label')
# nextlabel.place(x=300, y=400, height=100, width=100)

buttonframe.pack(padx = 20, fill='x')

control_frame = tk.Frame(root)
control_frame.pack(pady=20)

clear_btn = tk.Button(control_frame, text='Wyczyść', command=clear_text)
clear_btn.grid(row=0, column=0, padx=5)

show_btn = tk.Button(control_frame, text='Pokaż', command=show_text)
show_btn.grid(row=0, column=1, padx=5)

color_btn = tk.Button(control_frame, text='Zmień kolor', command=change_background)
color_btn.grid(row=0, column=2, padx=5)

copy_btn = tk.Button(control_frame, text='Kopiuj do Label', command=copy_to_label)
copy_btn.grid(row=0, column=3, padx=5)

count_btn = tk.Button(root, text='Kliknij mnie', command=count_click)
count_btn.pack(pady=10)

counter_label = tk.Label(root, text='Licznik: 0', font=('Arial', 14))
counter_label.pack()

nextlabel = tk.Label(root, text='Label', bg='white')
nextlabel.place(x=300, y=450, height=50, width=150)

root.mainloop()