import tkinter as tk
from tkinter import messagebox
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.expression = ''

        self.create_widgets()

        self.bind_mouse_events()

    def create_widgets(self):
        self.display = tk.Entry(
            self.root,
            font=("Arial", 20),
            borderwidth=5,
            relief="ridge",
            justify="right"
        )
        self.display.pack(fill="x", padx=10, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        for i in range(4):
            self.button_frame.columnconfigure(i, weight=1)

        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
            ("√", 4, 0), ("x²", 4, 1), ("C", 4, 2)
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(
                self.button_frame,
                text=text,
                font=("Arial", 16),
                width=5,
                height=2,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

        self.mouse_label = tk.Label(
            self.root,
            text="Pozycja myszy: ",
            font=("Arial", 10)
        )
        self.mouse_label.pack(pady=10)

    def on_button_click(self, value):
        if value == "=":
            self.calculate()

        elif value == "C":
            self.clear()

        elif value == "√":
            self.square_root()

        elif value == "x²":
            self.square()

        else:
            self.expression += str(value)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)

    def calculate(self):
        try:
            result = eval(self.expression)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
            self.expression = str(result)
        except Exception:
            messagebox.showerror("Błąd", "Niepoprawne wyrażenie")
            self.expression = ""

    def clear(self):
        """Czyści wyświetlacz"""
        self.expression = ""
        self.display.delete(0, tk.END)

    def square_root(self):
        """Oblicza pierwiastek z aktualnej liczby"""
        try:
            value = float(self.display.get())
            result = math.sqrt(value)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
            self.expression = str(result)
        except:
            messagebox.showerror("Błąd", "Nie można obliczyć pierwiastka")

    def square(self):
        """Podnosi liczbę do kwadratu"""
        try:
            value = float(self.display.get())
            result = value ** 2
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
            self.expression = str(result)
        except:
            messagebox.showerror("Błąd", "Błąd operacji")

    def bind_mouse_events(self):
        self.root.bind("<Motion>", self.on_mouse_move)
        self.root.bind("<Button-3>", self.show_context_menu)

    def on_mouse_move(self, event):
        text = f"Pozycja myszy: ({event.x}, {event.y})"
        self.mouse_label.config(text=text)

    def show_context_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Wyczyść", command=self.clear)
        menu.add_command(label="Oblicz", command=self.calculate)
        menu.add_separator()
        menu.add_command(label="Informacja o pozycji",
                         command=lambda: messagebox.showinfo(
                             "Pozycja myszy",
                             f"Kliknięto w:\nX={event.x}\nY={event.y}"
                         ))

        # Pokazujemy menu w pozycji kursora (globalnej)
        menu.tk_popup(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()