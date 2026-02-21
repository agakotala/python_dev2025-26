import tkinter as tk

root = tk.Tk()
root.title('Wysrodkowane')

window_height = 200
window_width = 300
screen_width = root.winfo_screenwidth()    # pobranie rozmiaru ekranu
screen_height = root.winfo_screenheight()
print(f'Wysokosc ekranu: {screen_height}\nszerokosc ekranu {screen_width}')
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

root.mainloop()